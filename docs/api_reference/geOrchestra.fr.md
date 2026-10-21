## [Classe geOrchestra](https://github.com/georchestra/geo-utils/blob/main/geOrchestra/geOrchestra.py)

```python
from geOrchestra import geOrchestra

server = "https://demo.georchestra.org"
username = "testadmin"
password = "testadmin"

geOr_api = geOrchestra(server, username, password)
```

`server` est l’URL de base de l’instance, sans barre oblique finale. Le paramètre `verifytls` est facultatif et vaut `True` par défaut : il contrôle la vérification des certificats TLS pour les trois clients. Pour un serveur de développement utilisant un certificat autosigné, vous pouvez la désactiver :

```python
geOr_api = geOrchestra(server, username, password, verifytls=False)
```

Ne désactivez pas cette vérification en production. Le client fournit :

| Attribut | Client | Rôle |
| --- | --- | --- |
| `geOr_api.gn` | `GN_API` | API du catalogue et des métadonnées GeoNetwork |
| `geOr_api.console` | `Console_api` | API Console pour les utilisateurs, organisations et rôles |
| `geOr_api.geoserver` | `GeoServerCloud` | Client de la dépendance GeoServer Cloud |

L’initialisation crée immédiatement les trois clients de service. Le client GeoNetwork effectue des requêtes pendant l’initialisation pour lire les informations du site et obtenir un cookie XSRF. Les options propres à GeoNetwork, comme le préfixe d’URL ou la méthode d’obtention du cookie XSRF, nécessitent d’instancier `GN_API` directement.