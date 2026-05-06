#!/bin/bash
set -x

# Import thesauri from the list stored in config/thesauri.csv file
# into your catalog

# Set your own values here. This is not a CLI, sorry
CATALOG=https://mydomain.georchestra.org/geonetwork
CATALOGUSER=testadmin
CATALOGPASS=testadmin
CONFIG_FOLDER="./config"

# Prepare the connection : get xsrf token
rm -f /tmp/cookie;
curl -s -c /tmp/cookie -o /dev/null \
  -X GET \
  -H "Accept: application/json" \
  "$CATALOG/srv/api/me";
TOKEN=`grep XSRF-TOKEN /tmp/cookie | grep /geonetwork | cut -f 7`;

curl \
  -X GET \
  -H "Accept: application/json" \
  -H "X-XSRF-TOKEN: $TOKEN" --user $CATALOGUSER:$CATALOGPASS -b /tmp/cookie \
  "$CATALOG/srv/api/me"
# MUST return user details

# # Upload GEMET thesaurus
# curl \
#     -X PUT \
#     -H  "accept: text/xml" \
#     -H  "Content-Type: application/json" -b /tmp/cookie \
#     -H  "X-XSRF-TOKEN: $TOKEN"  --user $CATALOGUSER:$CATALOGPASS \
#     "$CATALOG/srv/api/registries/vocabularies?url=https%3A%2F%2Fraw.githubusercontent.com%2Fgeonetwork%2Futil-gemet%2Fmaster%2Fthesauri%2Fgemet.rdf&registryUrl=&registryType=&type=external&dir=theme" 

# # Upload INSPIRE themes thesaurus
# curl \
#     -X PUT \
#     -H  "accept: text/xml" \
#     -H  "Content-Type: application/json" -b /tmp/cookie \
#     -H  "X-XSRF-TOKEN: $TOKEN"  --user $CATALOGUSER:$CATALOGPASS \
#     "$CATALOG/srv/api/registries/vocabularies?url=&registryLanguage=en&registryLanguage=fr&registryUrl=http%3A%2F%2Finspire.ec.europa.eu%2Ftheme&registryType=re3gistry&type=external&dir=theme" 

# # Upload INSPIRE metadata codelist protocols thesaurus
# curl \
#     -X PUT \
#     -H  "accept: text/xml" \
#     -H  "Content-Type: application/json" -b /tmp/cookie \
#     -H  "X-XSRF-TOKEN: $TOKEN"  --user $CATALOGUSER:$CATALOGPASS \
#     "$CATALOG/srv/api/registries/vocabularies?url=&registryLanguage=en&registryLanguage=fr&registryUrl=https://inspire.ec.europa.eu/metadata-codelist/ProtocolValue&registryType=re3gistry&type=external&dir=theme" 


while IFS="," read -r source cat params
do
  echo "Importing thesaurus $source $cat"
  # echo $params
  curl \
    -X PUT \
    -H  "accept: text/xml" \
    -H  "Content-Type: application/json" -b /tmp/cookie \
    -H  "X-XSRF-TOKEN: $TOKEN"  --user $CATALOGUSER:$CATALOGPASS \
    "$CATALOG/srv/api/registries/vocabularies?$params" 
done < <(tail -n +2 $CONFIG_FOLDER/thesauri.csv)