# geo-utils

This repository contains many tips/scripts/librairies in order to simplify administration/automation of geOrchestra plateform.

If you have any ideas to develop/which you could create a new issue here : https://github.com/georchestra/geo-utils/issues

## Python module

There is also a python module in order to script actions in geOrchestra plateform

To install it : 
```
pip install git+https://github.com/georchestra/geo-utils/ 
```
(you might need --break-system-packages option)

to try it:
```
In [1]: from geOrchestra import geOrchestra
In [2]: username = "testadmin"
In [3]: password = "testadmin"
In [4]: url = "https://demo.georchestra.org/"
In [5]: geo_api = geOrchestra(url, username, password)
In [6]: geo_api.console.getroles()
Out[6]: '[{"uniqueIdentifier":[......]
In [7]: geo_api.gn.search_keyword("velo")
Out[7]: ......
```
## Dependencies 

geoserverCloud librairy https://github.com/camptocamp/python-geoservercloud

can be installed with `pip install geoservercloud`

## Documentation

The Python library documentation is built with MkDocs and Material, following the geOrchestra documentation template structure.

Install the documentation dependencies and preview the site locally:

```bash
python -m pip install -r mkdocs_requirements.txt
mkdocs serve
```

Then open http://127.0.0.1:8000/. The English documentation sources are in [`docs/`](docs/index.en.md), with the [getting started guide](docs/user_guide/getting_started.en.md) and [API reference](docs/technical_guides/api_reference.en.md).


## Extra useful lib

https://github.com/jdev-org/georchestra-ldap-py
