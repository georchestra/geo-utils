## [geOrchestra class](https://github.com/georchestra/geo-utils/blob/main/geOrchestra/geOrchestra.py) 

```python
from geOrchestra import geOrchestra

server = "https://demo.georchestra.org"
username = "testadmin"
password = "testadmin"

geOr_api = geOrchestra(server, username, password)
```

`server` is the instance base URL without a trailing slash. The client provides:

| Attribute | Client | Purpose |
| --- | --- | --- |
| `geOr_api.gn` | `GN_API` | GeoNetwork catalog and metadata API |
| `geOr_api.console` | `Console_api` | Console user, organization, and role API |
| `geOr_api.geoserver` | `GeoServerCloud` | GeoServer Cloud dependency client |

Initialization immediately creates all three service clients. The GeoNetwork client makes requests during initialization to read site details and obtain an XSRF cookie. The top-level constructor takes no optional service configuration.