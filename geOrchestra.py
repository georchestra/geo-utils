import json
import time
if __name__ == "__main__":
    # adding local file
    from meta_apis import Ask_gn_api
    from meta_apis.meta_manipulation import Meta_manipulation
    from console import Console_api
else:
    # adding relative path
    from .meta_apis import Ask_gn_api
    from .meta_apis.meta_manipulation import Meta_manipulation
    from .console import Console_api

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
    server = "https://georchestra-127-0-0-1.nip.io"

    geOrchestra_api = geOrchestra(server, username, password)
    geOrchestra_api.gn.generate_xsfr()
    print(geOrchestra_api.gn.get_metadataxml("4b5f8e1b-de37-47cd-9203-37a59f318b09"))



#    usertestadmin = json.loads(geOrchestra_api.console.getusers(uid="testadmin"))
#    user_org = json.loads(geOrchestra_api.console.getorgs(uid=usertestadmin["org"]))
#    print(usertestadmin)
#    usertestadmin["orgObj"] = user_org
#    usertestadmin["description"] = "This is another test for console API"

#    print(geOrchestra_api.console.updateuserdetails(uid="testadmin",json=json.dumps(usertestadmin)))

    all_havests = geOrchestra_api.gn.get_harvests()
    # get only filesystem harvests
    test2 = list(filter(lambda x: x["@type"] == "filesystem", all_havests))
    # take only the activate ones
    test3 = list(filter(lambda x: x["options"]["status"] == "active", test2)) # reverse is inactive
    # loop to make them local
    for harvest in test3:
        print(harvest["site"]["uuid"])
        print(geOrchestra_api.gn.make_harvest_local(harvest["site"]["uuid"]))
        name = input("pass enter to continue:")
        time.sleep(2)