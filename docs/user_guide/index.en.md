# User guide

This guide is for Python scripts that need to call geOrchestra services using an account that is authorized for the requested operation.

## Available clients

The `geOrchestra` client exposes three attributes:

- `geOr_api.gn` for GeoNetwork catalog and metadata operations.
- `geOr_api.console` for Console users, organizations, and roles.
- `geOr_api.geoserver` for the [GeoServer Cloud Python client](https://github.com/camptocamp/python-geoservercloud).

The first two clients are implemented in this repository. GeoServer Cloud behavior is provided by its separate dependency.

Continue with [Getting started](getting_started.md) to install the package and make a first request.
