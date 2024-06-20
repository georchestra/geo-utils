#!/usr/bin/env python3



import sys
import os
import fileinput
import csv
import base64


LINELENGTH = 76

SEPARATOR = ';'
JOINER = '|'
QUOTECHAR = '"'

"""
out put should look like that for an user

version: 1

dn: uid=jeanmi,ou=users,dc=georchestra,dc=org
objectClass: georchestraUser
objectClass: inetOrgPerson
objectClass: organizationalPerson
objectClass: person
objectClass: shadowAccount
objectClass: top
cn: jean mi
sn: Jeanmi
uid: jeanmi
georchestraObjectIdentifier:: ZWY5MTAwNzYtZWMyMi00ZTA0LTlmNjMtYjQ3MjcyNGQxZj
 My
givenName: JeanMi
mail: jean-mi@georchestra.org
userPassword:: xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
 xxx=

###
for an organisation it should look like 
version: 1

dn: cn=ORGA,ou=orgs,dc=georchestra,dc=org
objectClass: groupOfMembers
objectClass: top
cn: ORGA
member: uid=jeanmi,ou=users,dc=georchestra,dc=org
o:: xxxxxxxxxx
ou: ORGA
seeAlso: o=ORGA,ou=orgs,dc=georchestra,dc=org

-

dn: o=ORGA,ou=orgs,dc=georchestra,dc=org
objectClass: georchestraOrg
objectClass: organization
objectClass: top
o: ORGA
businessCategory: Other
georchestraObjectIdentifier:: 
jpegPhoto:: 
labeledURI: https://www.orga.fr/
postalAddress: 


"""

def findgoodorgsname(oldorg):
    fin = open('neworgs.csv')
    found = False
    for line in fin:
        l = line.split(',')
        shortname = l[0]
        fullname = l[1]

        if fullname.lower() in oldorg.lower():
            found = shortname
            break

    return found
def getnewrole(old_roles):
    fin = open('newroles.csv')
    found = False

    for line in fin:
        l = line.split(",")
        source = l[0]
        dest = l[1]

        if source == old_roles:
            found = dest
    return found

def is_ascii(s):
    return all(ord(char) < 128 for char in s)

def main():

    csvreader = csv.reader(fileinput.input(mode='r'), delimiter=SEPARATOR, quotechar=QUOTECHAR, quoting=csv.QUOTE_ALL)
    first = True
    mode = None

    passwdsha = '4e9a134d304c3aece756c579da579237f4dc2f03a7572a69d51a2965988f0271'
    passb64 = base64.b64encode(bytes(passwdsha, 'utf-8')).decode('utf8')
    for row in csvreader:
        if first:
            # ignore first line

            # means it is user list
            if row[0] == "id,username,first_name,last_name, is_superuser ,email,is_active,organization":
                mode = 1
                user_orgs_export = open("out/user_orgs.ldif", "w")
                role_user_active = open("out/role_user_active.ldif", "w")
                role_admin_active = open("out/role_admin_active.ldif", "w")
            # groups
            elif row[0] == "id,slug ,title ,description":
                mode = 2
            # user groups, newuser_groups.csv
            elif row[0] == "p.id,p.username , first_name , last_name , is_superuser , p.email , is_active , organization ,pg.group_id,g.slug ,g.title,":
                mode = 3

            # FILE neworgs.csv
            elif row[0] == "shortname,fullname,Commentaire":
                mode = 4
            # FILE newroles.csv
            elif row[0] == "source groupe,destination role,description":
                mode = 5
            first = False
        elif mode == 1:
            #print(row[0])
            arrayline = row[0].split(",")
            username = arrayline[1].strip()
            if username == "":
                username = "\00"
            first_name = arrayline[2]
            if first_name == "":
                first_name = username
            last_name = arrayline[3]
            if last_name == "":
                last_name = username
            is_superuser = arrayline[4]
            if is_superuser == "":
                is_superuser = "\00"
            email = arrayline[5]
            if email == "":
                email = "\00"
            is_active = arrayline[6]
            if is_active == "":
                is_active = "\00"

            organization = arrayline[7]

            command = os.popen('uuidgen')
            newuuid = base64.b64encode(bytes(command.read().strip() , 'utf-8')).decode('utf8')
            command.close()

            line = "-\n"
            line += "\n"
            line += "dn: uid=%s,ou=users,dc=georchestra,dc=org\n" % (username)
            line += "objectClass: georchestraUser\n"
            line += "objectClass: inetOrgPerson\n"
            line += "objectClass: organizationalPerson\n"
            line += "objectClass: person\n"
            line += "objectClass: shadowAccount\n"
            line += "objectClass: top\n"
            line += "cn: %s %s\n" % (first_name , last_name )
            line += "sn: %s\n" % (last_name)
            line += "uid: %s\n" % (username)
            line += "georchestraObjectIdentifier:: %s\n" % (newuuid)
            line += "givenName: %s\n" % (first_name)
            line += "mail: %s\n" % (email)
            line += "userPassword:: %s\n" % (passb64)
            line += "\n"

            sys.stdout.write(line)


            if organization != "\00":
                orgs = "-\n"
                orgs += "\n"
                orgs += "dn: cn=%s,ou=orgs,dc=georchestra,dc=org\n" % (organization)
                orgs += "changetype: modify\n"
                orgs += "add: member\n"
                orgs += "member: uid=%s,ou=users,dc=georchestra,dc=org\n" % (username)
                orgs += "\n"

                user_orgs_export.write(orgs)

            if is_superuser == "true":
                newadminrole = "-\n"
                newadminrole += "\n"
                newadminrole += "dn: cn=ADMINISTRATOR,ou=roles,dc=georchestra,dc=org\n"
                newadminrole += "changetype: modify\n"
                newadminrole += "add: member\n"
                newadminrole += "member: uid=%s,ou=users,dc=georchestra,dc=org\n" % (username)
                newadminrole += "\n"

                role_admin_active.write(newadminrole)

            if is_active == "true":
                # create the USER roles for this user
                newuserole = "-\n"
                newuserole += "\n"
                newuserole += "dn: cn=USER,ou=roles,dc=georchestra,dc=org\n"
                newuserole += "changetype: modify\n"
                newuserole += "add: member\n"
                newuserole += "member: uid=%s,ou=users,dc=georchestra,dc=org\n" % (username)
                newuserole += "\n"

                role_user_active.write(newuserole)
            #sys.stdout.write('\n')

        elif mode == 2:
            print("groups")
        elif mode == 3:
            # this part to add user into their roles
            # p.id,p.username , first_name , last_name , is_superuser , p.email , is_active , organization ,pg.group_id,g.slug ,g.title,
            arrayline = row[0].split(",")
            username = arrayline[1]
            old_roles = arrayline[9]

            if old_roles != "":
                newrole = getnewrole(old_roles.lower())
                line = "-\n"
                line += "\n"
                line += "dn: cn=%s,ou=roles,dc=georchestra,dc=org\n" % (newrole)
                line += "changetype: modify\n"
                line += "add: member\n"
                line += "member: uid=%s,ou=users,dc=georchestra,dc=org\n" % (username)
                line += "\n"

                sys.stdout.write(line)

                if newrole == False:
                    print("something is wrong if goes here")
                    print(old_roles)
                    break

        elif mode == 4:
            # file neworgs.csv, creation of the different orgs that are empty (without users for now)
            arrayline = row[0].split(",")
            shortname = arrayline[0]
            fullname = base64.b64encode(bytes(arrayline[1], 'utf-8')).decode('utf8')
            # always empty
            #description=

            command = os.popen('uuidgen')
            newuuid = base64.b64encode(bytes(command.read().strip(), 'utf-8')).decode('utf8')
            command.close()

            #print(shortname, fullname)

            line = "-\n"
            line += "\n"
            line += "dn: cn=%s,ou=orgs,dc=georchestra,dc=org\n" % (shortname)
            line += "objectClass: groupOfMembers\n"
            line += "objectClass: top\n"
            line += "cn: %s\n" % (shortname)
            line += "o:: %s\n" % (fullname)
            line += "ou: %s\n" % (shortname)
            line += "seeAlso: o=%s,ou=orgs,dc=georchestra,dc=org\n" % (shortname)
            line += "\n"
            line += "-\n"
            line += "\n"
            line += "dn: o=%s,ou=orgs,dc=georchestra,dc=org\n" % (shortname)
            line += "objectClass: georchestraOrg\n"
            line += "objectClass: organization\n"
            line += "objectClass: top\n"
            line += "o: %s\n" % (shortname)
            line += "businessCategory: Other\n"
            line += "georchestraObjectIdentifier:: %s\n" % (newuuid)
            line += "postalAddress: \00\n"
            line += "\n"

            sys.stdout.write(line)


        elif mode == 5:
            # FILE newroles.csv
            # this part is for the creation of new roles only
            # source groupe,destination role
            arrayline = row[0].split(",")
            rolesname = arrayline[1]
            description = base64.b64encode(bytes(arrayline[2], 'utf-8')).decode('utf-8')

            command = os.popen('uuidgen')
            newuuid = base64.b64encode(bytes(command.read().strip(), 'utf-8')).decode('utf8')
            command.close()

            line = "-\n"
            line += "\n"
            line += "dn: cn=%s,ou=roles,dc=georchestra,dc=org\n" % (rolesname)
            line += "objectClass: georchestraRole\n"
            line += "objectClass: groupOfMembers\n"
            line += "objectClass: top\n"
            line += "cn: %s\n" % (rolesname)
            line += "description: %s\n" % (description)
            line += "georchestraObjectIdentifier:: %s\n" % (newuuid)
            line += "\n"

            sys.stdout.write(line)
        else:
            print("Unsupported mode (probably wrong csv)")
    if mode == 1:
        user_orgs_export.close()
        role_user_active.close()
        role_admin_active.close()
    return 0


if __name__ == '__main__':
    main()
