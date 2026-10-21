"""List catalog metadata and report duplicate resource identifiers.

The script retrieves metadata from the GeoNetwork catalog and compares
non-empty resource identifiers found in each record's citation. Identifiers
are compared as exact values after surrounding whitespace is removed.

Set username and password, then run:
	python3 detection_duplicate_id_ressource.py

The report is written when duplicate resource identifiers or failed metadata
records are found. Failed records are included with their retrieval status,
but are excluded from identifier comparison and reported to stderr.
"""

import csv
import xml.etree.ElementTree as ET
from collections import defaultdict

from geOrchestra.meta_apis import GN_API, Metadata


SERVER = "https://demo.georchestra.org"
PREFIX_GN_URL = "/catalogue"
SUB_PORTAIL="craig"
DUPLICATES_CSV = "duplicated_idres_metadata.csv"
username = "testadmin"
password = "testadmin"


def read_xpath_text(metadata, xpath, index=1):
	xml_value = metadata.get_value_xpath(f"({xpath})[{index}]")
	if not xml_value:
		return ""
	return "".join(ET.fromstring(xml_value).itertext()).strip()


def read_resource_metadata(xml_text):
	metadata = Metadata(xml_text)
	if metadata.meta is None:
		raise ET.ParseError("Metadata XML could not be parsed")

	title_xpath = (
		"//*[local-name()='identificationInfo']//*[local-name()='citation']"
		"//*[local-name()='title']"
	)
	title_matches = metadata.meta.xpath(title_xpath, namespaces=metadata.ns)
	title = read_xpath_text(metadata, title_xpath) if title_matches else ""
	if not title:
		title_xpath = "//*[local-name()='title']"
		title_matches = metadata.meta.xpath(title_xpath, namespaces=metadata.ns)
		title = read_xpath_text(metadata, title_xpath) if title_matches else ""

	identifier_xpath = (
		"//*[local-name()='identificationInfo']//*[local-name()='citation']"
		"//*[local-name()='identifier']//*[local-name()='code']"
	)
	identifier_matches = metadata.meta.xpath(identifier_xpath, namespaces=metadata.ns)
	resource_identifiers = [
		value
		for index in range(1, len(identifier_matches) + 1)
		if (value := read_xpath_text(metadata, identifier_xpath, index))
	]

	return title, list(dict.fromkeys(resource_identifiers))


def metadata_with_progress(metadata_uuids):
	total = len(metadata_uuids)
	bar_width = 30
	print(f"\rRetrieving metadata: [{' ' * bar_width}] 0/{total}", end="", flush=True)
	for completed, metadata_uuid in enumerate(metadata_uuids, start=1):
		yield metadata_uuid
		filled = bar_width * completed // total
		bar = "#" * filled + " " * (bar_width - filled)
		print(
			f"\rRetrieving metadata: [{bar}] {completed}/{total}",
			end="\n" if completed == total else "",
			flush=True,
		)


def main():
	gn_api = GN_API(SERVER, username, password, prefix_gn_url=PREFIX_GN_URL)
	try:
		print(f"Getting all records in {SERVER}{PREFIX_GN_URL}/{SUB_PORTAIL}/ catalog")
		metadata_uuids = gn_api.get_all_catalog(steps=100, portal=SUB_PORTAIL)
		if not metadata_uuids:
			print("No metadata records were returned by the catalog API.")
			return 1
		print(f"Got {len(metadata_uuids)} metadata records.")
		records = []
		failed_records = []
		identifiers_to_records = defaultdict(list)

		for metadata_uuid in metadata_with_progress(metadata_uuids):
			xml_text = gn_api.get_metadataxml(metadata_uuid)
			if not xml_text:
				failed_records.append(metadata_uuid)
				records.append(
					{
						"metadata_uuid": metadata_uuid,
						"title": "",
						"resource_identifiers": [],
						"retrieval_status": "failed",
					}
				)
				continue

			try:
				title, identifiers = read_resource_metadata(xml_text)
			except ET.ParseError as error:
				print(f"Could not parse metadata {metadata_uuid}: {error}")
				failed_records.append(metadata_uuid)
				records.append(
					{
						"metadata_uuid": metadata_uuid,
						"title": "",
						"resource_identifiers": [],
						"retrieval_status": "failed",
					}
				)
				continue

			record = {
				"metadata_uuid": metadata_uuid,
				"title": title,
				"resource_identifiers": identifiers,
				"retrieval_status": "ok",
			}
			records.append(record)
			for identifier in identifiers:
				identifiers_to_records[identifier].append(record)

		duplicate_identifiers = {
			identifier: matching_records
			for identifier, matching_records in identifiers_to_records.items()
			if len({record["metadata_uuid"] for record in matching_records}) > 1
		}

		print(f"Processed {len(records)} metadata records.")
		print(f"Found {len(duplicate_identifiers)} resource identifiers shared by records.")
		if duplicate_identifiers or failed_records:
			with open(DUPLICATES_CSV, "w", newline="", encoding="utf-8") as output_file:
				writer = csv.DictWriter(
					output_file,
					fieldnames=[
						"metadata_uuid",
						"resource_identifier",
						"record_count",
						"title",
						"retrieval_status",
					],
				)
				writer.writeheader()
				for identifier, matching_records in sorted(duplicate_identifiers.items()):
					record_count = len({record["metadata_uuid"] for record in matching_records})
					for record in matching_records:
						writer.writerow(
							{
								"metadata_uuid": record["metadata_uuid"],
								"resource_identifier": identifier,
								"record_count": record_count,
								"title": record["title"],
								"retrieval_status": record["retrieval_status"],
							}
						)
				for uuid in failed_records:
					writer.writerow(
						{
							"metadata_uuid": uuid,
							"resource_identifier": "",
							"record_count": "",
							"title": "",
							"retrieval_status": "failed",
						}
					)

			print(f"Metadata report: {DUPLICATES_CSV}")
		else:
			print("No CSV report written because no duplicates or failed records were found.")
		if failed_records:
			print(
				f"Could not retrieve or parse {len(failed_records)} records; see errors above."
			)
		return 0
	finally:
		gn_api.closesession()


if __name__ == "__main__":
	main()
