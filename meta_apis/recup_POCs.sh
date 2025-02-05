#!/bin/bash

# Extract all the "Point of contact" blocks from a catalog's records
# Uses the API endpoint srv/api/registries/actions/entries/collect
# Scans the records, extracts the POCs. No deduplication here, this is pretty basic.
# (You can find an improved process, that includes deduplication, on 
# https://github.com/pi-geosolutions/POCs_xml2csv)

# Set your own values here. This is not a CLI, sorry
CATALOG=https://mydomain.georchestra.org/geonetwork
CATALOGUSER=testadmin
CATALOGPASS=testadmin

rm -f /tmp/cookie;
curl -s -c /tmp/cookie -o /dev/null \
  -X GET \
  -H "Accept: application/json" \
  "$CATALOG/srv/api/me";
TOKEN=`grep XSRF-TOKEN /tmp/cookie | grep /geonetwork | cut -f 7`;

curl -s -o /dev/null \
  -X GET \
  -H "Accept: application/json" \
  -H "X-XSRF-TOKEN: $TOKEN" --user $CATALOGUSER:$CATALOGPASS -b /tmp/cookie \
  "$CATALOG/srv/api/me"

# MUST return user details

# Run the search
curl -s -o /dev/null -X POST "$CATALOG/srv/api/search/records/_search?bucket=pocs" \
    -H 'Accept: application/json' \
    -H 'Content-Type: application/json;charset=utf-8' \
    -H "X-XSRF-TOKEN: $TOKEN" -c /tmp/cookie -b /tmp/cookie --user $CATALOGUSER:$CATALOGPASS \
    -d '{"from":0,"size":10,"query":{"query_string":{"query":"(documentStandard:\"iso19115-3.2018\") AND (isTemplate:\"n\")"}}}'
	
# The bucket name is arbitrary. This is where is will be "saved".
# The request can be inferred by using the search UI and looking the network requests. Look for query > query value

# Then the results from the search need to be set as selected
curl -s -o /dev/null -X PUT "$CATALOG/srv/api/selections/pocs" -H "accept: application/json" \
  -H "X-XSRF-TOKEN: $TOKEN" -c /tmp/cookie -b /tmp/cookie --user $CATALOGUSER:$CATALOGPASS
    
# Check the status of the current selections
curl -s -o /dev/null -X GET "$CATALOG/srv/api/selections" -H "accept: application/json" \
  -H "X-XSRF-TOKEN: $TOKEN" -c /tmp/cookie -b /tmp/cookie --user $CATALOGUSER:$CATALOGPASS
    
# Run the process over the selected records
# Output is written to pocs.xml file
curl -X GET "$CATALOG/srv/api/registries/actions/entries/collect?bucket=pocs&xpath=.//cit:CI_Responsibility&identifierXpath=.//cit:electronicMailAddress/*/text()" \
    -H  "accept: application/xml"\
    -H "X-XSRF-TOKEN: $TOKEN" -c /tmp/cookie -b /tmp/cookie --user $CATALOGUSER:$CATALOGPASS \
    -o pocs.xml
