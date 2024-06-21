
from meta_apis.ask_gn_api import Ask_gn_api
from meta_apis.meta_manipulation import Meta_manipulation
from console.console import Console_api
import json

class geOrchestra:
    def __init__(self, server, username, password):
        self.server = server
        self.username = username
        self.password = password
        self.gn = Ask_gn_api(server, username, password)
        self.console = Console_api(server, username, password)
    
if __name__ == "__main__":
    # Set up your username and password:
    username = 'testadmin'
    password = 'testadmin'

    # Set up your server and the authentication URL:
    server = "https://georchestra-127-0-1-1.traefik.me"

    geOrchestra_api = geOrchestra(server, username, password)
    geOrchestra_api.gn.generate_xsfr()
    print(geOrchestra_api.gn.getmetadataxml("4b5f8e1b-de37-47cd-9203-37a59f318b09"))



    usertestadmin = json.loads(geOrchestra_api.console.getusers(uid="testadmin"))
    user_org = json.loads(geOrchestra_api.console.getorgs(uid=usertestadmin["org"]))
    print(usertestadmin)
    usertestadmin["orgObj"] = user_org
    usertestadmin["description"] = "This is another test for console API"

    print(geOrchestra_api.console.updateuserdetails(uid="testadmin",json=json.dumps(usertestadmin)))

