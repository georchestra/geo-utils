import requests
import json

class Console_api:
    def __init__(self, server, username, password):
        self.server = server
        self.username = username
        self.password = password
        self.session = requests.Session()
        self.headers = {'Accept': 'application/json'}

    def getusers(self, uid="", filter=None):
        url = self.server + "/console/private/users/" + uid
        response = self.session.get(url,
                                    auth=(self.username, self.password),
                                    headers=self.headers,
                                    )

        if (response.status_code == 200):
            return response.text

    def updateuserdetails(self, uid, json):
        url = self.server + "/console/private/users/" + uid

        response = self.session.put(url,
                                    data=json,
                                    auth=(self.username, self.password),
                                    headers=self.headers)
        # print(response)
        if (response.status_code == 200):
            return response.text

    def createnewuser(self, org, sn, givenname, mail, description):
        newuser = {"pending": "false",
                   "org": org,
                   "manager": "",
                   "sn": sn,
                   "givenName": givenname,
                   "mail": mail,
                   "description": description,
                   }
        print(newuser)
        url = self.server + "/console/private/users"

        response = self.session.post(url,
                                     data=json.dumps(newuser),
                                     auth=(self.username, self.password),
                                     headers=self.headers)

        if (response.status_code == 200):
            return response.text
        else:
            return "Error while creating the user"

    def getorgs(self, uid="", filter=None):
        url = self.server + "/console/private/orgs/" + uid
        response = self.session.get(url,
                                    auth=(self.username, self.password),
                                    headers=self.headers)

        if (response.status_code == 200):
            return response.text

    def getroles(self, uid=""):
        headers = {'Accept': 'application/json'}
        url = self.server + "/console/private/roles/" + uid
        response = self.session.get(url,
                                    auth=(self.username, self.password),
                                    headers=headers)

        if (response.status_code == 200):
            return response.text


if __name__ == "__main__":
    # Set up your username and password:
    username = 'testadmin'
    password = 'testadmin'

    # Set up your server and the authentication URL:
    server = "https://georchestra-127-0-1-1.traefik.me"

    console_API = Console_api(server, username, password)
    # print(console_API.getusers())
    # print(console_API.getroles())
    # print(console_API.getorgs())
    usertestadmin = json.loads(console_API.getusers(uid="testadmin"))
    # print(usertestadmin["description"])
    user_org = json.loads(console_API.getorgs(uid=usertestadmin["org"]))
    # print(user_org)
    usertestadmin["orgObj"] = user_org

    usertestadmin["description"] = "This is a test of changing the description of the user testadmin"

    # open("testadmin2.json", "w").write(json.dumps(usertestadmin))
    print(usertestadmin["uid"])
    print(console_API.updateuserdetails(uid=usertestadmin["uid"], json=json.dumps(usertestadmin)))

    print(console_API.createnewuser(org="PSC", sn="testapi", givenname="test", mail="testsss@georchestra.org",
                                    description="This user was created with the api"))
