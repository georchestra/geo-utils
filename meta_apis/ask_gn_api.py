import json
import requests
import re
import urllib3
import sys

if __name__ == "__main__":
    # adding local file
    from meta_manipulation import Meta_manipulation


# disable https checks (for testing or development server)
urllib3.disable_warnings()


class Ask_gn_api:
    def __init__(
        self, server, username, password, verifytls=True, prefix_gn_url="/geonetwork"
    ):
        self.server = server
        self.username = username
        self.password = password
        self.xsrf_token = ""
        self.session = None
        self.verifytls = verifytls
        self.id_node_gn = ""
        self.prefix_gn_url = prefix_gn_url
        self.get_gnversion()
        self.generate_xsfr()

    def get_gnversion(self):
        url = self.server + self.prefix_gn_url + "/srv/api/site"
        self.session = requests.Session()
        response = requests.Session().get(
            url, headers={"Accept": "application/json"}, verify=self.verifytls
        )
        self.session.close()
        rsp = json.loads(response.text)
        self.id_node_gn = rsp["node/id"]
        return rsp

    # put this right before function
    def generate_xsfr(self):
        authenticate_url = self.server + self.prefix_gn_url + "/srv/fre/info?type=me"

        # To generate the XRSF token, send a post request to the following URL: http://localhost:8080/geonetwork/srv/eng/info?type=me
        self.session = requests.Session()
        response = self.session.post(authenticate_url, verify=self.verifytls)
        self.session.close()
        # print(response.cookies)
        # Extract XRSF token
        self.xsrf_token = response.cookies.get("XSRF-TOKEN", path=self.prefix_gn_url)
        if self.xsrf_token:
            print("The XSRF Token is:", self.xsrf_token)
        else:
            print(response.text)
            print("Unable to find the XSRF token")

    def get_metadataxml(self, uuid):
        headers = {
            "Accept": "application/xml",
            "X-XSRF-TOKEN": self.xsrf_token,
        }
        url = self.server + self.prefix_gn_url + "/srv/api/records/" + uuid

        self.session = requests.Session()
        response = self.session.get(
            url,
            auth=(self.username, self.password),
            headers=headers,
            verify=self.verifytls,
        )
        self.session.close()
        if response.status_code == 200:
            return response.text

    # possible value for uuidprocessing : NOTHING , OVERWRITE , GENERATEUUID
    def upload_metadata(
        self, metadata, groupid="100", uuidprocessing="GENERATEUUID", publish=False
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

        # session = requests.Session()

        # print(username, password, xsrf_token, server, params, headers)
        # Send a put request to the endpoint
        self.session = requests.Session()
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
        self.session.close()

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
            return True, answer_api
        elif response.status_code == 400 :
            answer_api = json.loads(response.text)
            print(answer_api)
            return False, answer_api
        else:
            print(response)
            print(response.text)
            raise Exception(f"Échec Geonetwork ({response.status_code}) : {response.text}")
            return False, response.text

    def get_thesaurus_dict(self):
        url = self.server + self.prefix_gn_url + "/srv/fre/thesaurus?_content_type=json"
        # no needed to authenticate this is public
        self.session = requests.Session()
        response = self.session.get(url, verify=self.verifytls)
        self.session.close()
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
        self.session = requests.Session()
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
        self.session.close()
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
        self.session = requests.Session()
        response = self.session.delete(
            url,
            auth=(self.username, self.password),
            headers=headers,
            verify=self.verifytls,
        )
        self.session.close()
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
        self.session = requests.Session()
        response = self.session.get(
            url,
            auth=(self.username, self.password),
            headers=headers,
            verify=self.verifytls,
        )
        self.session.close()
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

        self.session = requests.Session()
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
        self.session.close()

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

        self.session = requests.Session()

        response = self.session.get(
            url,
            cookies={"XSRF-TOKEN": self.xsrf_token},
            auth=(self.username, self.password),
            headers=headers,
            verify=self.verifytls,
        )
        self.session.close()

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
            cookies={"XSRF-TOKEN": self.xsrf_token},
            auth=(self.username, self.password),
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
            cookies={"XSRF-TOKEN": self.xsrf_token},
            auth=(self.username, self.password),
            headers=headers,
            verify=self.verifytls,
        )

        return json.loads(response.text)

    def feed_search_bucket(self, name, uuid):
        # PUT /selections/{bucket}?uuid=123&uuid=456
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
            cookies={"XSRF-TOKEN": self.xsrf_token},
            auth=(self.username, self.password),
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
            cookies={"XSRF-TOKEN": self.xsrf_token},
            auth=(self.username, self.password),
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

    api_obj = Ask_gn_api(
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
