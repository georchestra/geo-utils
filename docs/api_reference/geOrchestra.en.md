## [geOrchestra class](https://github.com/georchestra/geo_utils/blob/main/geOrchestra/geOrchestra.py#L9)

```python
from geOrchestra import geOrchestra

server = "https://demo.georchestra.org"
username = "testadmin"
password = "testadmin"

geOr_api = geOrchestra(server, username, password)
```

`server` is the instance base URL without a trailing slash. The optional `verifytls` parameter defaults to `True` and controls TLS certificate verification for all four clients. For a development server using a self-signed certificate, you can disable verification:

```python
geOr_api = geOrchestra(server, username, password, verifytls=False)
```

Do not disable certificate verification in production. The client provides:

| Attribute | Client | Purpose |
| --- | --- | --- |
| `geOr_api.gn` | `GN_API` | GeoNetwork catalog and metadata API |
| `geOr_api.console` | `Console_api` | Console user, organization, and role API |
| `geOr_api.console` | `Console_api` | Console user, organization, and role API |
| `geOr_api.maelstro` | `Maelstro` | Maelstro metadata and layer copy API |
| `geOr_api.geoserver` | `GeoServerCloud` | GeoServer Cloud dependency client |

Initialization immediately creates all four service clients. The GeoNetwork client makes requests during initialization to read site details and obtain an XSRF cookie. GeoNetwork-specific options, such as the URL prefix or XSRF cookie retrieval method, require instantiating `GN_API` directly.