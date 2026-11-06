## [Classe geOrchestra](https://github.com/georchestra/geo_utils/blob/main/geOrchestra/geOrchestra.py#L9)

```python
from geOrchestra import geOrchestra

server = "https://demo.georchestra.org"
username = "testadmin"
password = "testadmin"

geOr_api = geOrchestra(server, username, password)
```

`server` est l’URL de base de l’instance, sans barre oblique finale. Le paramètre `verifytls` est facultatif et vaut `True` par défaut : il contrôle la vérification des certificats TLS. Le paramètre `with_geoserver` est facultatif et vaut `True` par défaut ; définissez-le sur `False` pour ignorer l’initialisation du client GeoServer. Si l’extra `geoservercloud` n’est pas installé, `geoserver` vaut `None`.

```python
geOr_api = geOrchestra(server, username, password, verifytls=False)
```

Ne désactivez pas cette vérification en production. Le client fournit :

| Attribut | Client | Rôle |
| --- | --- | --- |
| `geOr_api.gn` | `GN_API` | API du catalogue et des métadonnées GeoNetwork |
| `geOr_api.console` | `Console_api` | API Console pour les utilisateurs, organisations et rôles |
| `geOr_api.geoserver` | `GeoServerCloud` ou `None` | Client GeoServer Cloud facultatif |

L’initialisation crée les clients GeoNetwork et Console. Le client GeoNetwork effectue des requêtes pendant l’initialisation pour lire les informations du site et obtenir un cookie XSRF. L’initialisation de GeoServer est facultative. Les options propres à GeoNetwork, comme le préfixe d’URL ou la méthode d’obtention du cookie XSRF, nécessitent d’instancier `GN_API` directement.