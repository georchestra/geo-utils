

## GeoServer

The top-level client's `geoserver` attribute is a `GeoServerCloud` instance from the [GeoServer Cloud Python library](https://github.com/camptocamp/python-geoservercloud). The wrapper builds it with the instance URL's `/geoserver/` endpoint and the supplied credentials.

See the [GeoServer Cloud library documentation](https://camptocamp.github.io/python-geoservercloud/) for its methods, options, and supported workflows. For example, its client can create a workspace:

```python
geOr_api.geoserver.create_workspace("example")
```

This call changes the server and requires an account with appropriate GeoServer permissions.