import json
import requests
import re
import urllib3
import sys
import xmltodict
import time

if __name__ == "__main__":
    # adding local file
    from meta_manipulation import Meta_manipulation


# disable https checks (for testing or development server)
urllib3.disable_warnings()


class GN_API:
    def __init__(
        self,
        server,
        username,
        password,
        verifytls=True,
        prefix_gn_url="/geonetwork",
        xsrf_via_get=False,
    ):
        self.server = server
        self.username = username
        self.password = password
        self.xsrf_token = ""
        self.session = requests.Session()
        self.session.auth = (username, password)
        self.verifytls = verifytls
        self.id_node_gn = ""
        self.prefix_gn_url = prefix_gn_url
        self.get_gnversion()
        self.generate_xsfr(use_get=xsrf_via_get)

    def get_gnversion(self):
        url = self.server + self.prefix_gn_url + "/srv/api/site"

        response = requests.Session().get(
            url, headers={"Accept": "application/json"}, verify=self.verifytls
        )
        rsp = json.loads(response.text)
        self.id_node_gn = rsp["node/id"]
        return rsp

    # put this right before function
    def generate_xsfr(self, use_get=False):
        # use_get=True:  GET  /srv/api/me          (current GeoNetwork REST API)
        # use_get=False: POST /srv/fre/info?type=me (legacy endpoint, kept for
        #                older GeoNetwork instances where /srv/api/me might not
        #                behave as expected)
        # Either way, this call's only purpose is to make the server set the
        # XSRF-TOKEN cookie: the response status itself is not meaningful (both
        # endpoints can answer with an error status depending on the server/
        # security-proxy setup, while still setting the cookie).
        if use_get:
            authenticate_url = self.server + self.prefix_gn_url + "/srv/api/me"
            response = self.session.get(
                authenticate_url,
                headers={"Accept": "application/json"},
                verify=self.verifytls,
            )
        else:
            authenticate_url = self.server + self.prefix_gn_url + "/srv/fre/info?type=me"
            response = self.session.post(authenticate_url, verify=self.verifytls)

        # Extract XRSF token
        tmp_xsrf = response.cookies.get("XSRF-TOKEN", path=self.prefix_gn_url)
        if tmp_xsrf:
            self.xsrf_token = tmp_xsrf
            print("The XSRF Token is:", self.xsrf_token)
        else:
            print(response.text)
            print("Unable to find the XSRF token")

    def get_all_catalog(self, steps=100, portal=None):
        # using CSW url /geonetwork/srv/fre/csw?service=CSW&version=2.0.2&request=GetRecords&typeNames=csw:Record&resultType=results&elementSetName=brief&maxRecords=10&startPosition=1
        # portal: uuid of a sub-portal (e.g. "Donnees-geographiques-OFB", see
        # /srv/api/sources) to restrict the CSW query to that sub-catalog only,
        # instead of the whole GeoNetwork instance.
        headers = {
            "Accept": "application/xml",
            "X-XSRF-TOKEN": self.xsrf_token,
        }
        csw_path = f"/{portal}/fre/csw" if portal else "/srv/fre/csw"

        meta_list_to_return = []
        start_position = 1
        while True:
            url_meta = (
                self.server
                + self.prefix_gn_url
                + csw_path
                + f"?service=CSW&version=2.0.2&request=GetRecords&typeNames=csw:Record&resultType=results&elementSetName=brief&maxRecords={steps}&startPosition={start_position}"
            )
            response_meta = self.session.get(
                url_meta,
                auth=(self.username, self.password),
                headers=headers,
                verify=self.verifytls,
            )
            if response_meta.status_code != 200:
                return meta_list_to_return or None

            search_results = xmltodict.parse(response_meta.text).get(
                "csw:GetRecordsResponse", {}
            ).get("csw:SearchResults")
            if not search_results:
                return meta_list_to_return or None

            records = search_results.get("csw:BriefRecord") or []
            if isinstance(records, dict):
                records = [records]
            for meta in records:
                identifier = meta.get("dc:identifier")
                if isinstance(identifier, dict):
                    meta_list_to_return.append(identifier["#text"])
                elif isinstance(identifier, str):
                    meta_list_to_return.append(identifier)

            returned = int(search_results.get("@numberOfRecordsReturned", len(records)))
            if returned == 0:
                break

            start_position += steps
            # slow down a bit
            time.sleep(0.1)

        return meta_list_to_return or None

    def get_metadataxml(self, uuid):
        headers = {
            "Accept": "application/xml",
            "X-XSRF-TOKEN": self.xsrf_token,
        }
        url = self.server + self.prefix_gn_url + "/srv/api/records/" + uuid

        response = self.session.get(
            url,
            auth=(self.username, self.password),
            headers=headers,
            verify=self.verifytls,
        )
        if response.status_code == 200:
            return response.text

    def get_metadata_mef_zip(self, uuid, with_related=True, timeout=120):
        # Full MEF (Metadata Exchange Format) export of a record: XML content
        # plus privileges, categories and attachments. Suitable for backup and
        # re-import via upload_metadata(uuidprocessing="OVERWRITE").
        headers = {
            "Accept": "application/zip",
            "X-XSRF-TOKEN": self.xsrf_token,
        }
        url = (
            self.server
            + self.prefix_gn_url
            + f"/srv/api/records/{uuid}/formatters/zip"
            + f"?withRelated={str(with_related).lower()}"
        )
        response = self.session.get(
            url,
            auth=(self.username, self.password),
            headers=headers,
            verify=self.verifytls,
            timeout=timeout,
        )
        if response.status_code == 200:
            return response.content
        return None

    # possible value for uuidprocessing : NOTHING , OVERWRITE , GENERATEUUID
    def upload_metadata(
        self,
        metadata,
        groupid: str = "100",
        uuidprocessing: str = "GENERATEUUID",
        publish: bool = False,
    ):
        headers = {
            "Accept": "application/json",
            "X-XSRF-TOKEN": self.xsrf_token,
        }

        # Set the parameters
        params = {
            "metadataType": "METADATA",
            "uuidProcessing": uuidprocessing,
            "transformWith": "_none_",
            "group": groupid,
            "publishToAll": str(publish).lower(),
        }

        # print(username, password, xsrf_token, server, params, headers)
        # Send a put request to the endpoint
        response = self.session.post(
            self.server + self.prefix_gn_url + "/srv/api/records",
            json=params,
            cookies={"XSRF-TOKEN": self.xsrf_token},
            params=params,
            auth=(self.username, self.password),
            headers=headers,
            files={"file": metadata},
            verify=self.verifytls,
        )


        if response.status_code == 200 or response.status_code == 201:
            answer_api = json.loads(response.text)
            print(
                "Upload metadatahere : "
                + self.server
                + self.prefix_gn_url
                + "/srv/fre/catalog.search#/metadata/"
                + answer_api["metadataInfos"][list(answer_api["metadataInfos"])[0]][0][
                    "uuid"
                ]
            )
            # print(answer_api)
            return answer_api
        elif response.status_code == 400:
            answer_api = json.loads(response.text)
            print(answer_api)
            return False
        else:
            print(response)
            print(response.text)
            return False

    def get_thesaurus_dict(self, thesaurus_key=None):
        url = self.server + self.prefix_gn_url + "/srv/fre/thesaurus?_content_type=json"
        # no needed to authenticate this is public
        response = self.session.get(url, verify=self.verifytls)

        if thesaurus_key is None:
            return json.loads(response.text)[0]
        else:
            for th in json.loads(response.text)[0]:
                if th["key"] == thesaurus_key:
                    return th

    def searchin_thesaurus_dict(self, keyword: str = "", thesaurus_key=False):
        url = f"{self.server}{self.prefix_gn_url}/srv/api/registries/vocabularies/search?q={keyword}&lang=fre&rows=10&start=0"

        if isinstance(thesaurus_key, str):
            url += f"&thesaurus={thesaurus_key}"
        if isinstance(thesaurus_key, list) or isinstance(thesaurus_key, dict):
            for key in thesaurus_key:
                url += f"&thesaurus={key}"
        if isinstance(thesaurus_key, bool):
            # select all thesaurus
            for th in self.get_thesaurus_dict():
                url += f"&thesaurus={th['key']}"
        # no needed to authenticate this is public
        headers = {"Accept": "application/json", "X-XSRF-TOKEN": self.xsrf_token}
        response = self.session.get(url, headers=headers, verify=self.verifytls)

        return json.loads(response.text)

    # not working yet
    def add_thesaurus_dict(self, filename):
        headers = {
            "Accept": "application/json",
            "X-XSRF-TOKEN": self.xsrf_token,
            "Origin": "http://" + self.server,
            "Referer": "http://"
            + self.server
            + self.prefix_gn_url
            + "/srv/fre/admin.console",
        }  #

        # Set the parameters
        params = {
            "_csrf": self.xsrf_token,
            "url": "",
            "registryUrl": "",
            "registryType": "",
            "type": "local",
            "dir": "theme",
        }  #  'stylesheet': '_none_',

        cookies = {
            "XSRF-TOKEN": self.xsrf_token,
        }
        response = self.session.post(
            self.server
            + self.prefix_gn_url
            + "/srv/api/registries/vocabularies?_csrf="
            + self.xsrf_token,
            auth=(self.username, self.password),
            headers=headers,
            cookies=cookies,
            data=params,
            verify=self.verifytls,
            files=[
                ("file", (filename, open(filename, "rb").read(), "application/rdf+xml"))
            ],
        )

        req = response.request
        print(
            "{}\n{}\r\n{}\r\n\r\n{}".format(
                "-----------START-----------",
                req.method + " " + req.url,
                "\r\n".join("{}: {}".format(k, v) for k, v in req.headers.items()),
                req.body,
            )
        )
        print(response.request)
        print("uploaded new thesaurus")
        print(response)
        print(response.text)

    # format of name [internal|external].[theme|place|...].[name]
    def delete_thesaurus_dict(self, name):
        headers = {
            "Accept": "application/json",
            "X-XSRF-TOKEN": self.xsrf_token,
        }

        url = (
            self.server
            + self.prefix_gn_url
            + "/srv/api/registries/vocabularies/"
            + name
        )
        response = self.session.delete(
            url,
            auth=(self.username, self.password),
            headers=headers,
            verify=self.verifytls,
        )

        if response.status_code == 200:
            return response.text
        else:
            return "Error while deleting thesaurus reason " + response.text

    def get_harvests(self):
        headers = {"Accept": "application/json", "X-XSRF-TOKEN": self.xsrf_token}
        url = (
            self.server
            + self.prefix_gn_url
            + "/srv/fre/admin.harvester.list?_content_type=json&id=-1"
        )
        response = self.session.get(
            url,
            auth=(self.username, self.password),
            headers=headers,
            verify=self.verifytls,
        )

        # print(response)

        if response.status_code == 200:
            return json.loads(response.text)
        else:
            return "Error"

    def make_harvest_local(self, uuid):
        headers = {"Accept": "application/json", "X-XSRF-TOKEN": self.xsrf_token}
        url = (
            self.server
            + self.prefix_gn_url
            + "/srv/api/harvesters/"
            + uuid
            + "/assign?source="
            + self.id_node_gn
        )

        # can take forever to answer if there is a lot of connected metadatas to the harvest
        # 1h timeout should be enough
        response = self.session.post(
            url,
            cookies={"XSRF-TOKEN": self.xsrf_token},
            auth=(self.username, self.password),
            headers=headers,
            verify=self.verifytls,
            timeout=3600,
        )


        print(response)
        if response.status_code == 204:
            return "Okay"
        else:
            # means the havert does not support the import of metadata (maybee empty or error
            return False

    def delete_harvest(self, id):
        headers = {"Accept": "application/json", "X-XSRF-TOKEN": self.xsrf_token}
        url = (
            self.server
            + self.prefix_gn_url
            + "/srv/fre/admin.harvester.remove?_content_type=json&id="
            + id
        )

        response = self.session.get(
            url,
            cookies={"XSRF-TOKEN": self.xsrf_token},
            auth=(self.username, self.password),
            headers=headers,
            verify=self.verifytls,
        )


        return json.loads(response.text)

    def search_keyword(self, keywords):
        url = (
            self.server
            + self.prefix_gn_url
            + "/srv/api/search/records/_search?bucket=geoutilsbucket"
        )
        headers = {
            "Accept": "application/json",
            "X-XSRF-TOKEN": self.xsrf_token,
            "Origin": "http://" + self.server,
            "Referer": "http://"
            + self.server
            + self.prefix_gn_url
            + "/srv/fre/admin.console",
        }
        params = {
            "aggregations": {},
            "from": 0,
            "size": 18,
            "sort": [{"createDate": "desc"}],
            "query": {
                "bool": {
                    "must": [
                        {
                            "query_string": {
                                "query": keywords.replace(":", "\\:"),
                                "default_operator": "AND",
                                "fields": [
                                    "resourceTitleObject.*^5",
                                    "tag.*^4",
                                    "resourceAbstractObject.*^3",
                                    "lineageObject.*^2",
                                    "any.*",
                                    "uuid",
                                ],
                            }
                        }
                    ],
                    "must_not": [
                        {
                            "query_string": {
                                "query": "resourceType:featureCatalog AND !resourceType:dataset AND !cl_level.key:dataset"
                            }
                        }
                    ],
                    "should": [],
                    "filter": [{"terms": {"isTemplate": ["n"]}}],
                }
            },
            "track_total_hits": True,
            "_source": ["uuid", "id", "title", "link", "linkProtocol"],
        }

        response = self.session.post(
            url,
            json=params,
            cookies={"XSRF-TOKEN": self.xsrf_token},
            params=params,
            auth=(self.username, self.password),
            headers=headers,
            verify=self.verifytls,
        )

        if response.status_code == 200:
            return json.loads(response.text)
        else:
            print(response)
            print(response.text)
            return False

    def get_search_buckets(self):
        # get all existing search buckets
        # get /selections
        headers = {"Accept": "application/json", "X-XSRF-TOKEN": self.xsrf_token}
        url = self.server + self.prefix_gn_url + "/srv/api/selections"

        response = self.session.get(
            url,
            headers=headers,
            verify=self.verifytls,
        )

        return json.loads(response.text)

    def get_search_bucket(self, name):
        # get the content of a search bucket from its name
        headers = {"Accept": "application/json", "X-XSRF-TOKEN": self.xsrf_token}
        url = self.server + self.prefix_gn_url + "/srv/api/selections/" + name

        response = self.session.get(
            url,
            headers=headers,
            verify=self.verifytls,
        )

        return json.loads(response.text)

    def feed_search_bucket(self, name, uuid):
        headers = {"Accept": "application/json", "X-XSRF-TOKEN": self.xsrf_token}
        # print(type(uuid))
        feeduuid = ""
        if type(uuid) == str:
            feeduuid += uuid
        elif type(uuid) == dict or type(uuid) == list:
            for index, uid in enumerate(uuid):
                # print(index, uid)
                if index == 0:
                    feeduuid += uid
                else:
                    feeduuid += "&uuid=" + uid
        # print(feeduuid)
        url = (
            self.server
            + self.prefix_gn_url
            + "/srv/api/selections/"
            + name
            + "?uuid="
            + feeduuid
        )

        response = self.session.put(
            url,
            headers=headers,
            verify=self.verifytls,
        )

        return json.loads(response.text)

    def purge_search_bucket(self, name, uuid=None):
        headers = {"Accept": "application/json", "X-XSRF-TOKEN": self.xsrf_token}
        if uuid is not None:
            # print(type(uuid))
            feeduuid = ""
            if type(uuid) == str:
                feeduuid += uuid
            elif type(uuid) == dict or type(uuid) == list:
                for index, uid in enumerate(uuid):
                    # print(index, uid)
                    if index == 0:
                        feeduuid += uid
                    else:
                        feeduuid += "&uuid=" + uid
            url = (
                self.server
                + self.prefix_gn_url
                + "/srv/api/selections/"
                + name
                + "?uuid="
                + feeduuid
            )
        else:
            url = self.server + self.prefix_gn_url + "/srv/api/selections/" + name

        response = self.session.delete(
            url,
            headers=headers,
            verify=self.verifytls,
        )

        return json.loads(response.text)

    # before using this function you need to create and feed a bucket
    # of search with the function feed_search_bucket
    # you can check its content with get_search_bucket()
    def batch_edit_search_and_replace(
        self,
        bucket_name,
        search,
        replace,
        regex_flags="",
        use_regex="false",
        update_date_stamp="false",
    ):
        # POST /geonetwork/srv/api/processes/db/search-and-replace?bucket=e101&diffType=&regexpFlags=mi&replace=test&search=test&useRegexp=true
        # documentation https://docs.geonetwork-opensource.org/4.4/api/the-geonetwork-api/#loop-on-search-results-and-apply-changes-processing-and-batch-editing
        # regex flags :
        #   i: enables case insensitive matching
        #   c: disables case insensitive matching
        #   n: allows the period to match the newline character
        #   m: enables multiline mode

        headers = {"Accept": "application/json", "X-XSRF-TOKEN": self.xsrf_token}
        url = (
            self.server
            + self.prefix_gn_url
            + "/srv/api/processes/db/search-and-replace?bucket="
            + bucket_name
            + "&diffType="
            + "&regexpFlags="
            + regex_flags
            + "&replace="
            + replace
            + "&search="
            + search
            + "&useRegexp="
            + use_regex
            + "&updateDateStamp="
            + update_date_stamp
        )
        params = {"headers": {"accept": "application/xml"}}

        response = self.session.post(
            url,
            json=params,
            cookies={"XSRF-TOKEN": self.xsrf_token},
            params=params,
            auth=(self.username, self.password),
            headers=headers,
            verify=self.verifytls,
        )

        return json.loads(response.text)
    # action = ['replace', 'add', 'delete' ]
    def batch_edit_xpath(self, bucket_name, xpath , value, update_timestamps: bool = False,  action='replace', condition=""):
        headers = {"Accept": "application/json", "X-XSRF-TOKEN": self.xsrf_token}
        url = self.server + self.prefix_gn_url + f"/srv/api/records/batchediting?bucket={bucket_name}&diffType=&updateDateStamp={str(update_timestamps).lower()}"
        params = {"headers": {"accept": "application/xml"}, }
        build_xpath = [{'xpath': xpath, 'condition': condition, 'value': f"<gn_{action}>{value}</gn_{action}>"}]
        response = self.session.put(
            url,
            json=build_xpath,
            params=params,
            headers=headers,
            verify=self.verifytls,
        )
        return json.loads(response.text)

    def get_record_privileges(self, uuid):
        # groupOwner/isPublishedToAll of a record, so a full-document
        # overwrite (see upload_metadata uuidProcessing=OVERWRITE) can be
        # resubmitted with the same sharing settings instead of resetting them.
        headers = {"Accept": "application/json", "X-XSRF-TOKEN": self.xsrf_token}
        url = self.server + self.prefix_gn_url + "/srv/api/search/records/_search"
        body = {
            "query": {"terms": {"_id": [uuid]}},
            "_source": ["groupOwner"],
        }
        response = self.session.post(
            url,
            json=body,
            headers=headers,
            auth=(self.username, self.password),
            verify=self.verifytls,
        )
        if response.status_code != 200:
            return None
        hits = response.json().get("hits", {}).get("hits", [])
        if not hits:
            return None
        hit = hits[0]
        return {
            "groupOwner": hit.get("_source", {}).get("groupOwner"),
            "isPublishedToAll": bool(hit.get("isPublishedToAll", False)),
        }

    def closesession(self):
        self.session.close()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("You should specify the xml file to upload like that :")
        print(" python3 ask_gn_api.py sample_meta.xml")
        exit()
    file_to_update = sys.argv[1]

    print("Will upload the file " + file_to_update)

    # Set up your username and password:
    username = "testadmin"
    # username = "admin"
    password = "testadmin"
    # password = "admin"

    # Set up your server and the authentication URL:
    server = "https://georchestra-127-0-0-1.nip.io"  # test with geOrchestra
    # server = "http://localhost" # test with geonetwork
    final_server = server

    api_obj = GN_API(
        server=server, username=username, password=password, verifytls=False
    )

    print(api_obj.get_gnversion())
    api_obj.generate_xsfr()

    # add exemple thesaurus to the GN
    api_obj.add_thesaurus_dict("exemple.rdf")

    # read / add thesaurus to sample metadata and upload metadata to the remote GN
    f = open(file_to_update)
    meta_to_upload = f.read()
    f.close()
    meta_to_upload_updated = Meta_manipulation.add_thesaurus(
        meta_to_upload,
        title="Category",
        server=final_server,
        thesaurus_value="test1",
        local_thesaurus_name="exemple",
    )

    api_obj.upload_metadata(
        metadata=meta_to_upload_updated, uuidprocessing="OVERWRITE", publish=True
    )

    list_thesaurus = api_obj.get_thesaurus_dict()

    for thesauru in list_thesaurus[0]:
        print("Key name : " + thesauru["key"])
    print(api_obj.delete_thesaurus_dict("external.theme.eu.europa.language"))

    api_obj.closesession()
