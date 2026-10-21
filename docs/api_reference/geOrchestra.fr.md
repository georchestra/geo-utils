## [Classe geOrchestra](https://github.com/georchestra/geo-utils/blob/main/geOrchestra/geOrchestra.py)

```python
from geOrchestra import geOrchestra

server = "https://demo.georchestra.org"
username = "testadmin"
password = "testadmin"

geOr_api = geOrchestra(server, username, password)
```

`server` est l’URL de base de l’instance, sans barre oblique finale. Le client fournit :

| Attribut | Client | Rôle |
| --- | --- | --- |
| `geOr_api.gn` | `GN_API` | API du catalogue et des métadonnées GeoNetwork |
| `geOr_api.console` | `Console_api` | API Console pour les utilisateurs, organisations et rôles |
| `geOr_api.geoserver` | `GeoServerCloud` | Client de la dépendance GeoServer Cloud |

L’initialisation crée immédiatement les trois clients de service. Le client GeoNetwork effectue des requêtes pendant l’initialisation pour lire les informations du site et obtenir un cookie XSRF. Le constructeur principal n’accepte aucune configuration de service facultative.