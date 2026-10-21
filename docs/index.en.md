# geOrchestra Python library

`geOrchestra` is a Python package for scripting against geOrchestra services. It automates many actions needed for data platform administration.
It supports GeoNetwork, Console, and GeoServer automations.

The package is part of [geo-utils](https://github.com/georchestra/geo-utils), a repository of geOrchestra utilities and administration scripts. This guide covers the Python library only.

## API documentation

- [API reference](api_reference.md): available service methods and important limitations.

## Getting started

## Requirements

- Python 3.9 or newer
- A geOrchestra instance reachable from the machine running your script (e.g. https://demo.georchestra.org/)
- A username and password with permissions for the services and operations you will use

## Install

Install the package directly from GitHub:

```bash
python3 -m pip install "git+https://github.com/georchestra/geo-utils.git"
```

The package metadata declares `requests`, `python-dotenv`, and `geoservercloud` as dependencies. If you are installing into an externally managed system Python, use a virtual environment as followed :

```bash
python3 -m venv venv
source venv/bin/activate
python3 -m pip install "git+https://github.com/georchestra/geo-utils.git"
```
## Samples

Start to play :
```python
import json
import os
from geOrchestra import geOrchestra

server = "https://demo.georchestra.org"
username = "testadmin"
password = "testadmin"

geOr_api = geOrchestra(server, username, password)

# GeoNetwork: get record identifiers and fetch one metadata XML document
record_ids = geOr_api.gn.get_all_catalog(steps=50)
print(f"Catalog records: {len(record_ids or [])}")
if record_ids:
    metadata_xml = geOr_api.gn.get_metadataxml(record_ids[0])

# Console: read a user; Console methods return JSON text on success
user_json = geOr_api.console.getusers(uid=username)
if user_json:
    user = json.loads(user_json)
    print(user.get("uid"), user.get("org"))

# Console: list roles (also returned as JSON text)
roles_json = geOr_api.console.getroles()
if roles_json:
    roles = json.loads(roles_json)
    print(roles)
```

All services are available from the same `geOr_api` instance. 


### GeoServer

The wrapper creates `geOr_api.geoserver` using the same instance URL and credentials. Its methods are provided by the [GeoServer Cloud Python library](https://github.com/camptocamp/python-geoservercloud); for example, create a workspace:

```python
geOr_api.geoserver.create_workspace("example")
```

See the [upstream library documentation](https://camptocamp.github.io/python-geoservercloud/) for its other methods.

### Console

Console methods are also available directly from the wrapper. For example, create a user in an existing organization:

```python
result = geOr_api.console.createnewuser(
    org="PSC",
    sn="Example",
    givenname="User",
    mail="example@example.org",
    description="Created by an automation script",
)
print(result)
```

## Connection details

For development purposes, you can disable TLS checks and customize the GeoNetwork URL prefix:

```python
from geOrchestra.meta_apis import GN_API

gn = GN_API(
    server=server,
    username=username,
    password=password,
    verifytls=False,
    prefix_gn_url="/catalogue",
)
```

## Go further 

[API reference](api_reference.md): available service methods and important limitations.


