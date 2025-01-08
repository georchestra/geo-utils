import json
import requests
import re
import urllib3
import sys

if __name__ == "__main__":
    # adding local file
    from meta_manipulation import Meta_manipulation


# disable https checks (for testing or development server)
# urllib3.disable_warnings()


class Ask_gn_api:
    def __init__(self, server, username, password ):
        self.server = server
        self.username = username
        self.password = password
        self.xsrf_token = ""
        self.session = None

    def get_gnversion(self):
        url = self.server + '/geonetwork/srv/api/site'
        self.session = requests.Session()
        response = requests.Session().get(url, headers={'Accept': 'application/json'})
        self.session.close()
        return response.text

    # put this right before function
    def generate_xsfr(self):
        print("toto")
        authenticate_url = self.server + '/geonetwork/srv/fre/info?type=me'

        # To generate the XRSF token, send a post request to the following URL: http://localhost:8080/geonetwork/srv/eng/info?type=me
        self.session = requests.Session()
        response =  self.session.post(authenticate_url)
        self.session.close()
        # print(response.cookies)
        # Extract XRSF token
        self.xsrf_token = response.cookies.get("XSRF-TOKEN", path="/geonetwork")
        if self.xsrf_token:
            print("The XSRF Token is:", self.xsrf_token)
        else:
            print(response.text)
            print("Unable to find the XSRF token")

    def get_metadataxml(self, uuid):
        headers = {'Accept': 'application/xml',
                   'X-XSRF-TOKEN': self.xsrf_token,
                   }
        url = self.server + "/geonetwork/srv/api/records/"+uuid

        self.session = requests.Session()
        response =  self.session.get(url,
                                     auth=(self.username, self.password),
                                     headers=headers,
                                    )
        self.session.close()
        if(response.status_code == 200):
            return response.text
    # possible value for uuidprocessing : NOTHING , OVERWRITE , GENERATEUUID
    def upload_metadata(self, metadata, groupid='100', uuidprocessing='GENERATEUUID', publish=False):
        headers = {'Accept': 'application/json',
                   'X-XSRF-TOKEN': self.xsrf_token,
        }

        # Set the parameters
        params = {
            'metadataType': 'METADATA',
            'uuidProcessing': uuidprocessing,
            'transformWith': '_none_',
            'group': groupid,
            'publishToAll': str(publish).lower()
        }

        # session = requests.Session()

        # print(username, password, xsrf_token, server, params, headers)
        # Send a put request to the endpoint
        self.session = requests.Session()
        response =  self.session.post( self.server + '/geonetwork/srv/api/records',
         json=params,
         cookies={'XSRF-TOKEN': self.xsrf_token},
         params=params,
         auth = (self.username, self.password),
         headers=headers,
         files={'file': metadata}
         )
        self.session.close()

        if response.status_code == 200 or response.status_code == 201 :
            answer_api = json.loads(response.text)
            print("Upload metadatahere : " + self.server + "/geonetwork/srv/fre/catalog.search#/metadata/" +
                   answer_api['metadataInfos'][list(answer_api['metadataInfos'])[0]][0]['uuid'])
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

    def get_thesaurus_dict(self):
        url = self.server + "/geonetwork/srv/fre/thesaurus?_content_type=json"
        # no needed to authenticate this is public
        self.session = requests.Session()
        response =  self.session.get(url)
        self.session.close()
        return json.loads(response.text)

    # not working yet
    def add_thesaurus_dict(self, filename):
        headers = {
                   'Accept': 'application/json',
                  'X-XSRF-TOKEN': self.xsrf_token,
                   'Origin': 'http://'+self.server,
                   'Referer': 'http://'+self.server+'/geonetwork/srv/fre/admin.console',
        } #

        # Set the parameters
        params = {
            '_csrf': self.xsrf_token,
            'url': '',
            'registryUrl' : '',
            'registryType': '',
            'type': 'local',
            'dir': 'theme',
        } #  'stylesheet': '_none_',

        cookies = {
            'XSRF-TOKEN':self.xsrf_token,
        }
        self.session = requests.Session()
        response =  self.session.post( self.server + '/geonetwork/srv/api/registries/vocabularies?_csrf='+self.xsrf_token,
                                      auth=(self.username, self.password),
                                     headers=headers, cookies=cookies, data=params,
                                     files=[('file', (filename, open(filename,'rb').read(), 'application/rdf+xml'))]
                                     )
        self.session.close()
        req = response.request
        print('{}\n{}\r\n{}\r\n\r\n{}'.format(
            '-----------START-----------',
            req.method + ' ' + req.url,
            '\r\n'.join('{}: {}'.format(k, v) for k, v in req.headers.items()),
            req.body,
        ))
        print(response.request)
        print("uploaded new thesaurus")
        print(response)
        print(response.text)

    # format of name [internal|external].[theme|place|...].[name]
    def delete_thesaurus_dict(self, name):
        headers = {'Accept': 'application/json',
                   'X-XSRF-TOKEN': self.xsrf_token,
                   }

        url = self.server + "/geonetwork/srv/api/registries/vocabularies/" + name
        self.session = requests.Session()
        response =  self.session.delete(url,
                                       auth=(self.username, self.password),
                                       headers=headers,
                                       )
        self.session.close()
        if response.status_code == 200:
            return response.text
        else:
            return "Error while deleting thesaurus reason "+response.text

    def closesession(self):
        self.session.close()


if __name__ == "__main__":
    if( len(sys.argv) < 2):
        print('You should specify the xml file to upload like that :')
        print(' python3 ask_gn_api.py sample_meta.xml')
        exit()
    file_to_update = sys.argv[1]

    print("Will upload the file " + file_to_update)

    # Set up your username and password:
    username = 'testadmin'
    username = "admin"
    password = 'testadmin'
    password = "admin"

    # Set up your server and the authentication URL:
    server = "https://georchestra-127-0-1-1.traefik.me" # test with geOrchestra
    server = "http://localhost" # test with geonetwork
    final_server = server

    api_obj = Ask_gn_api(server=server, username=username, password=password)

    print(api_obj.get_gnversion())
    api_obj.generate_xsfr()

    # add exemple thesaurus to the GN
    api_obj.add_thesaurus_dict("exemple.rdf")

    # read / add thesaurus to sample metadata and upload metadata to the remote GN
    f = open(file_to_update)
    meta_to_upload = f.read()
    f.close()
    meta_to_upload_updated = Meta_manipulation.add_thesaurus(meta_to_upload, title="Category",
                                                         server=final_server, thesaurus_value="test1",
                                                         local_thesaurus_name="exemple"
                                                         )

    api_obj.upload_metadata(metadata=meta_to_upload_updated, uuidprocessing="OVERWRITE", publish=True)

    list_thesaurus = api_obj.get_thesaurus_dict()

    for thesauru in list_thesaurus[0]:
        print("Key name : " + thesauru['key'])
    print(api_obj.delete_thesaurus_dict("external.theme.eu.europa.language"))

    api_obj.closesession()
