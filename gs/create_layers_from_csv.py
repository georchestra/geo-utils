from geoserver.catalog import Catalog
import csv

cat = Catalog("https://georchestra-127-0-1-1.traefik.me/geoserver/rest", "admin", "admin")


with open('list_layers.csv', newline='') as csvfile:

    spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')

    for row in spamreader:
        # url,schema,table_name,gs_store
        url = row[0]
        schema = row[1]
        table_name = row[2]
        gs_store = row[3]

        print(url, schema, table_name, gs_store)
        try:
            workspace = cat.get_workspace(name=schema)
            # print(workspace)
            datastore = cat.get_store(name=gs_store, workspace=workspace)
            # print(datastore)
            cat.publish_featuretype(name=table_name, store=datastore, native_crs='EPSG:4326', srs='EPSG:4326')
        except:
            print("already exist or not exist in DB")
            pass
