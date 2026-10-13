# geOrchestra Python library

`geOrchestra` is a Python package for scripting against geOrchestra services. Its top-level client groups clients for GeoNetwork, the geOrchestra Console, and GeoServer Cloud.

The package is part of [geo-utils](https://github.com/georchestra/geo-utils), a repository of geOrchestra utilities and administration scripts. This guide covers the Python library only.

## Start here

- [User guide](user_guide/index.md): installation, connection setup, and a first request.
- [API reference](technical_guides/api_reference.md): available service methods and important limitations.

## Project information

- Python: 3.9 or newer
- Package: `geOrchestra`
- Repository: [georchestra/geo-utils](https://github.com/georchestra/geo-utils)
- Dependencies declared by the package: `requests`, `python-dotenv`, and `geoservercloud`

The library is an evolving collection of service wrappers. Check the reference and the source before relying on a method for a production workflow; not every operation has uniform error handling or return values.
