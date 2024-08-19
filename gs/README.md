
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
