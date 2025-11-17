
# Geoserver STUFF

## scripting
Using this librairie : https://pypi.org/project/gsconfig/

But there is only few functionality

```commandline
# create datastore from csv
python3 create_datastore_from_csv.py

# publish layer from existing datastore and existing data in database 
python3 create_layers_from_csv.py 

```

## usefull commands


To change all urls store in the datadir :

`sed -e "s#old.domain.name#new.domain.name#g" -i $(grep old.domain.name * -r -l)`

Clean gwc configuration when getting the error `Could not locate a layer or layer group with id` from wmts getcapabilities or geowebcache web configuration :

```
cd /mnt/geoserver_datadir
for i in $(grep '  <id>' gwc-layers/*.xml | sed 's/<id>//g' | sed 's/<\/id>//g' | cut -d':' -f2- | tr -d ' ') ; do
	NUMLINE=$(git grep $i | wc -l);
	#echo $i $NUMLINE
	if [ "$NUMLINE" == "1" ] ; then
	       echo "$i is not defined as layer";
	       FILE=$(grep $i * -r -l)
	       mv $FILE ${FILE}.back
	fi;
done
```
