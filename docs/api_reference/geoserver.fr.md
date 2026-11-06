## [GeoServer](https://github.com/camptocamp/python-geoservercloud)

L’attribut `geoserver` du client principal est une instance de `GeoServerCloud`, fournie par la [bibliothèque Python GeoServer Cloud](https://github.com/camptocamp/python-geoservercloud), lorsque la dépendance facultative est installée et que `with_geoserver` est activé. Sinon, cet attribut vaut `None`. Installez l’extra avec `python -m pip install "geOrchestra[geoserver]"`. Le wrapper construit le client avec l’endpoint `/geoserver/` de l’URL de l’instance et les identifiants fournis.

Consultez la [documentation de la bibliothèque GeoServer Cloud](https://camptocamp.github.io/python-geoservercloud/) pour ses méthodes, ses options et les cas d’usage pris en charge. Par exemple, son client peut créer un espace de travail :

```python
geOr_api.geoserver.create_workspace("example")
```

Cet appel modifie le serveur et nécessite un compte disposant des autorisations GeoServer appropriées.
