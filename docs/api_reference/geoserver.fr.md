## GeoServer

L’attribut `geoserver` du client principal est une instance de `GeoServerCloud`, fournie par la [bibliothèque Python GeoServer Cloud](https://github.com/camptocamp/python-geoservercloud). Le wrapper la construit avec l’endpoint `/geoserver/` de l’URL de l’instance et les identifiants fournis.

Consultez la [documentation de la bibliothèque GeoServer Cloud](https://camptocamp.github.io/python-geoservercloud/) pour ses méthodes, ses options et les cas d’usage pris en charge. Par exemple, son client peut créer un espace de travail :

```python
geOr_api.geoserver.create_workspace("example")
```

Cet appel modifie le serveur et nécessite un compte disposant des autorisations GeoServer appropriées.
