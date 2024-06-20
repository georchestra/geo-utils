from geoserver.catalog import Catalog
import csv

cat = Catalog("https://georchestra-127-0-1-1.traefik.me/geoserver/rest", "admin", "password")


with open('list_datastore.csv', newline='') as csvfile:

    spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')

    for row in spamreader:
        schema = row[0]

        print(schema)
        print(', '.join(row))


        url = "https://georchestra-127-0-1-1.traefik.me/geoserver/" + schema +"/"
        print(url)
        try:
            cat.create_workspace(name=schema, uri=url)
        except:
            print("Probably already exist")
            pass

        try:
            ds = cat.create_datastore(name=name_suffix, workspace=schema)
            ds.connection_parameters.update(
                 host="localhost",
                 port="5432",
                 database="gis",
                 user="postgres",
                 password="",
                 dbtype="postgis", schema=schema)
            cat.save(ds)


        except:
            print("Error creating the datastore")
            pass
