import requests
import json

class Console_api:
    def __init__(self, server, username, password):
        self.server = server
        self.username = username
        self.password = password
        self.session = requests.Session()
        self.headers = {'Accept': 'application/json'}

    # USERS
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

    def getusers(self, uid="", filter=None):
        url = self.server + "/console/private/users/" + uid
        response = self.session.get(url,
                                    auth=(self.username, self.password),
                                    headers=self.headers,
                                    )

        if (response.status_code == 200):
            return response.text
    def deluser(self, id):
        url = self.server + "/console/private/users/" + id
        response = self.session.delete(url,
                                    auth=(self.username, self.password),
                                    headers=self.headers,
                                    )
        if (response.status_code == 200):
            return response.text
        else:
            return "Error while deleting the user"

    def updateuserdetails(self, uid, json):
        url = self.server + "/console/private/users/" + uid

        response = self.session.put(url,
                                    data=json,
                                    auth=(self.username, self.password),
                                    headers=self.headers)
        # print(response)
        if (response.status_code == 200):
            return response.text

    # ORGS
    def createneworgs(self, name, shortName, orgType,
                      address="", description="", note="",
                      mail="", url="", b64logo="" ):

        neworg = {
            "name": name,
            "shortName": shortName,
            "orgType": orgType, # Association Company NGO Individual Other
            "address": address,
            "description": description,
            "note": note,
            "mail": mail,
            "url": url,
            "logo": b64logo
        }
        print(neworg)
        url = self.server + "/console/private/orgs"

        response = self.session.post(url,
                                     data=json.dumps(neworg),
                                     auth=(self.username, self.password),
                                     headers=self.headers)

        if (response.status_code == 200):
            return response.text
        else:
            print(response.status_code)
            return "Error while creating the org"
    def getorgs(self, uid="", filter=None):
        url = self.server + "/console/private/orgs/" + uid
        response = self.session.get(url,
                                    auth=(self.username, self.password),
                                    headers=self.headers)

        if (response.status_code == 200):
            return response.text

    def delorgs(self, id):
        url = self.server + "/console/private/orgs/" + id
        response = self.session.delete(url,
                                       auth=(self.username, self.password),
                                       headers=self.headers,
                                       )
        if (response.status_code == 200):
            return response.text
        else:
            return "Error while deleting the org"
    # def updateorgs(self):

    # ROLES
    def createnewroles(self, cn="NEWROLE", description="Default description"):
        newrole = {
            "cn": cn,
            "description": description,
        }
        url = self.server + "/console/private/roles"

        response = self.session.post(url,
                                     data=json.dumps(newrole),
                                     auth=(self.username, self.password),
                                     headers=self.headers)

        if (response.status_code == 200):
            return response.text
        else:
            print(response.status_code)
            return "Error while creating the role"

    def updaterolesuser(self, uuid="testadmin", cn="ROLE"):
        updateroles = {
            "users": [uuid],
            "PUT": [cn],
            "DELETE": []
        }
        url = self.server + "/console/private/roles_users"

        response = self.session.post(url,
                                     data=json.dumps(updateroles),
                                     auth=(self.username, self.password),
                                     headers=self.headers)

        if (response.status_code == 200):
            return response.text
        else:
            print(response.status_code)
            return "Error while updating the role's users"

    def getroles(self, uid=""):
        headers = {'Accept': 'application/json'}
        url = self.server + "/console/private/roles/" + uid
        response = self.session.get(url,
                                    auth=(self.username, self.password),
                                    headers=headers)

        if (response.status_code == 200):
            return response.text

    # def delroles(self):
    # def updateroles(self):

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
    print(console_API.deluser(id="testapi"))

    print(console_API.createneworgs(name="TESTAPI", shortName="testapi", orgType="Other"))
    print(console_API.delorgs(id="testapi"))