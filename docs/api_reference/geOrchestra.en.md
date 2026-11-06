## [geOrchestra class](https://github.com/georchestra/geo_utils/blob/main/geOrchestra/geOrchestra.py#L9)

```python
from geOrchestra import geOrchestra

server = "https://demo.georchestra.org"
username = "testadmin"
password = "testadmin"

geOr_api = geOrchestra(server, username, password)
```

`server` is the instance base URL without a trailing slash. The optional `verifytls` parameter defaults to `True` and controls TLS certificate verification. The optional `with_geoserver` parameter defaults to `True`; set it to `False` to skip GeoServer client initialization. If the `geoservercloud` extra is not installed, `geoserver` is set to `None`.

```python
geOr_api = geOrchestra(server, username, password, verifytls=False)
```

Do not disable certificate verification in production. The client provides:

| Attribute | Client | Purpose |
| --- | --- | --- |
| `geOr_api.gn` | `GN_API` | GeoNetwork catalog and metadata API |
| `geOr_api.console` | `Console_api` | Console user, organization, and role API |
| `geOr_api.geoserver` | `GeoServerCloud` or `None` | Optional GeoServer Cloud client |

Initialization creates the GeoNetwork and Console clients. The GeoNetwork client makes requests during initialization to read site details and obtain an XSRF cookie. GeoServer initialization is optional. GeoNetwork-specific options, such as the URL prefix or XSRF cookie retrieval method, require instantiating `GN_API` directly.