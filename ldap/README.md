# LDAP STUFF

## Creation User/roles/Orgs automation
script to create "automatically" from CSV new user/roles/orgs into georchestra LDAP
Usage of creatorldif.py

```
mkdir out
python3 creatorldif.py < newuser.csv > out/user.ldif
python3 creatorldif.py < neworgs.csv > out/new_orgs.ldif
python3 creatorldif.py < newroles.csv > out/roles.ldif
python3 creatorldif.py < newuser_groups.csv > out/usergroups.ldif


export URI="ldap://localhost:589"
exoprt CN="cn=admin,dc=georchestra,dc=org"
export SECRET="secret"

ldapadd -H ${URI}  -D ${CN} -w ${SECRET} < out/new_orgs.ldif
ldapadd -H ${URI}  -D ${CN} -w ${SECRET} < out/roles.ldif
ldapadd -H ${URI}  -D ${CN} -w ${SECRET} < out/user.ldif
ldapmodify -H ${URI}  -D ${CN} -w ${SECRET} < out/user_orgs.ldif
ldapmodify -H ${URI}  -D ${CN} -w ${SECRET} < out/role_user_active.ldif
ldapmodify -H ${URI}  -D ${CN} -w ${SECRET} < out/usergroups.ldif

```


To come update rotation policy password