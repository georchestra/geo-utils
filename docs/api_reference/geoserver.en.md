

## [GeoServer](https://github.com/camptocamp/python-geoservercloud)

The top-level client's `geoserver` attribute is a `GeoServerCloud` instance from the [GeoServer Cloud Python library](https://github.com/camptocamp/python-geoservercloud) when the optional dependency is installed and `with_geoserver` is enabled. Otherwise, the attribute is `None`. Install the extra with `python -m pip install "geOrchestra[geoserver]"`. The wrapper builds the client with the instance URL's `/geoserver/` endpoint and the supplied credentials.

See the [GeoServer Cloud library documentation](https://camptocamp.github.io/python-geoservercloud/) for its methods, options, and supported workflows. For example, its client can create a workspace:

```python
geOr_api.geoserver.create_workspace("example")
```

This call changes the server and requires an account with appropriate GeoServer permissions.