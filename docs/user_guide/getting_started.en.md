# Getting started

## Requirements

- Python 3.9 or newer
- A geOrchestra instance reachable from the machine running your script
- A username and password with permissions for the services and operations you will use

## Install

Install the package directly from GitHub:

```bash
python -m pip install "git+https://github.com/georchestra/geo-utils.git"
```

The package metadata declares `requests`, `python-dotenv`, and `geoservercloud` as dependencies. If you are installing into an externally managed system Python, use a virtual environment rather than overriding the operating system's package protections.

## Connect

Pass the base URL of the geOrchestra instance without a trailing slash. The client uses the supplied credentials for service requests. Keep credentials out of source control; the example reads them from environment variables.

```python
import json
import os
from geOrchestra import geOrchestra

server = os.environ["GEORCHESTRA_URL"].rstrip("/")
username = os.environ["GEORCHESTRA_USERNAME"]
password = os.environ["GEORCHESTRA_PASSWORD"]

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

All services are available from the same `geOr_api` instance. Its attributes are service clients, not a single normalized API: GeoNetwork, Console, and GeoServer Cloud each have their own method names and return types.

### Use the GeoServer Cloud client

The wrapper creates `geOr_api.geoserver` using the same instance URL and credentials. Its methods are provided by the [GeoServer Cloud Python library](https://github.com/camptocamp/python-geoservercloud); for example, create a workspace:

```python
geOr_api.geoserver.create_workspace("example")
```

This changes the server. Use a workspace name appropriate for your environment and an account allowed to administer GeoServer. See the [upstream library documentation](https://camptocamp.github.io/python-geoservercloud/) for its other methods.

### Make a Console change

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

This creates a real Console account. Check that the organization exists and that the credentials have the required permissions before running it.

Set the environment variables before running the script:

```bash
export GEORCHESTRA_URL="https://demo.georchestra.org"
export GEORCHESTRA_USERNAME="your-user"
export GEORCHESTRA_PASSWORD="your-password"
python your_script.py
```

## Connection details

Creating `geOrchestra(...)` creates the GeoNetwork, Console, and GeoServer Cloud clients. GeoNetwork initialization performs HTTP requests to inspect the catalog and obtain an XSRF token, so construction requires network access and a functioning GeoNetwork endpoint. The default GeoNetwork base path is `/geonetwork`.

The GeoNetwork client verifies TLS certificates by default. Set its `verifytls` option to `False` only for a controlled test environment with a known certificate issue; disabling verification weakens connection security. The top-level constructor does not expose GeoNetwork options, so instantiate `GN_API` directly only if you need to configure its path or TLS verification:

```python
from geOrchestra.meta_apis import GN_API

gn = GN_API(
    server=server,
    username=username,
    password=password,
    verifytls=True,
    prefix_gn_url="/geonetwork",
)
```

## Handle results carefully

Return values depend on the method. Some successful requests return JSON decoded into Python objects, some return response text, and some return `None`, `False`, or an error string on failure. Several methods do not check unsuccessful HTTP responses. Inspect and validate the result before using it in an automated or destructive workflow.

Console methods can create, update, and delete users, organizations, and role assignments. GeoNetwork methods can upload or modify metadata and harvest configuration. Use a least-privileged account, test against a non-production instance first, and confirm the target identifiers before making changes.
