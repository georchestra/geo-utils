# API reference

The package currently exposes these imports:

```python
from geOrchestra import geOrchestra
from geOrchestra.console import Console_api
from geOrchestra.meta_apis import GN_API, Meta_manipulation, Metadata, ThesaurusKeyword
```

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

## [GeoNetwork: `GN_API`](https://github.com/georchestra/geo-utils/blob/main/geOrchestra/meta_apis/gn_api.py)

Create the client directly to configure GeoNetwork-specific options:

```python
from geOrchestra.meta_apis import GN_API

server = "https://demo.georchestra.org"
username = "testadmin"
password = "testadmin"

gn = GN_API(
    server,
    username,
    password,
    verifytls=True,
    prefix_gn_url="/geonetwork",
    xsrf_via_get=False,
)
```

TLS certificate verification is enabled by default. `xsrf_via_get=True` uses `/srv/api/me`; the default uses the legacy `/srv/fre/info?type=me` endpoint to establish the XSRF cookie.

### Catalog and metadata

| Method | Purpose | Result notes |
| --- | --- | --- |
| `get_gnversion()` | Read GeoNetwork site details and node ID | Parsed JSON object |
| `get_all_catalog(steps=100, portal=None)` | Collect catalog record UUIDs using CSW paging | List of UUIDs, or `None` if no records/request failure |
| `get_metadataxml(uuid)` | Read a record XML document | XML text on HTTP 200; otherwise `None` |
| `get_metadata_mef_zip(uuid, with_related=True, timeout=120)` | Download a MEF ZIP export | ZIP bytes on HTTP 200; otherwise `None` |
| `upload_metadata(metadata, groupid="100", uuidprocessing="GENERATEUUID", publish=False)` | Upload a metadata file-like object; `uuidprocessing` supports the GeoNetwork values `NOTHING`, `OVERWRITE`, and `GENERATEUUID` | Parsed JSON on success; `False` for handled failures |
| `get_record_privileges(uuid)` | Read owner group and public visibility | Dictionary on success; otherwise `None` |



### Thesauri

| Method | Purpose |
| --- | --- |
| `get_thesaurus_dict(thesaurus_key=None)` | Retrieve thesaurus information, optionally for one key |
| `searchin_thesaurus_dict(keyword="", thesaurus_key=False)` | Search vocabulary terms, optionally restricted to thesaurus keys |
| `add_thesaurus_dict(filename)` | Upload a thesaurus file; implementation is experimental and prints request details |
| `delete_thesaurus_dict(name)` | Delete a thesaurus by its name/key |

### Harvests

| Method | Purpose | Result notes |
| --- | --- | --- |
| `get_harvests()` | List harvest configurations | Parsed JSON on success; `"Error"` otherwise |
| `make_harvest_local(uuid)` | Assign a harvest to the local GeoNetwork node | `"Okay"` or `False`; request timeout is up to one hour |
| `delete_harvest(id)` | Remove a harvest configuration | Parsed JSON response |

### Search selections and batch editing

| Method | Purpose |
| --- | --- |
| `search_keyword(keywords)` | Search records using the configured GeoNetwork query |
| `get_search_buckets()` | List saved search selections |
| `get_search_bucket(name)` | Read a selection by name |
| `feed_search_bucket(name, uuid)` | Add one or more record UUIDs to a selection |
| `purge_search_bucket(name, uuid=None)` | Remove selected UUIDs, or delete/clear the selection when UUIDs are omitted |
| `batch_edit_search_and_replace(bucket_name, search, replace, regex_flags="", use_regex="false", update_date_stamp="false")` | Search and replace metadata values for records in a selection |
| `batch_edit_xpath(bucket_name, xpath, value, update_timestamps=False, action="replace", condition="")` | Apply an XPath-based batch edit to records in a selection |

Batch edit methods operate on records in a search bucket. Review the bucket contents before applying changes. Response JSON is returned without a common error wrapper.

Call `closesession()` when finished with a standalone `GN_API` client to close its requests session.

## [Console: `Console_api`](https://github.com/georchestra/geo-utils/blob/main/geOrchestra/console/console.py)

The top-level client's `console` attribute is an instance of `Console_api`. It sends requests to `/console/private/...` using HTTP Basic authentication.

### Users

| Method | Purpose | Result notes |
| --- | --- | --- |
| `getusers(uid="", filter=None)` | Read a user by UID or request the users endpoint | Response text on HTTP 200; otherwise `None`. The `filter` parameter is currently unused. |
| `createnewuser(org, sn, givenname, mail, description)` | Create a user | Response text on HTTP 200; otherwise an error string. |
| `updateuserdetails(uid, json)` | Update a user; `json` is a JSON-encoded request body | Response text on HTTP 200; otherwise `None`. |
| `deluser(id)` | Delete a user | Response text on HTTP 200; otherwise an error string. |

### Organizations

| Method | Purpose | Result notes |
| --- | --- | --- |
| `getorgs(uid="", filter=None)` | Read an organization by UID or request the organizations endpoint | Response text on HTTP 200; otherwise `None`. The `filter` parameter is currently unused. |
| `createneworgs(name, shortName, orgType, address="", description="", note="", mail="", url="", b64logo="")` | Create an organization | `orgType` should be a Console-supported type such as `Association`, `Company`, `NGO`, `Individual`, or `Other`. Returns response text on HTTP 200; otherwise an error string. |
| `delorgs(id)` | Delete an organization | Response text on HTTP 200; otherwise an error string. |

### Roles

| Method | Purpose | Result notes |
| --- | --- | --- |
| `getroles(uid="")` | Read roles, optionally scoped by `uid` | Response text on HTTP 200; otherwise `None`. |
| `createnewroles(cn="NEWROLE", description="Default description")` | Create a role | Response text on HTTP 200; otherwise an error string. |
| `updaterolesuser(uuid="testadmin", cn="ROLE")` | Assign a role to a user | Response text on HTTP 200; otherwise an error string. |

These operations may require administrator privileges. Return values are response text, `None`, or an error string rather than a common response type. Check each result before continuing.

## GeoServer

The top-level client's `geoserver` attribute is a `GeoServerCloud` instance from the [GeoServer Cloud Python library](https://github.com/camptocamp/python-geoservercloud). The wrapper builds it with the instance URL's `/geoserver/` endpoint and the supplied credentials.

See the [GeoServer Cloud library documentation](https://camptocamp.github.io/python-geoservercloud/) for its methods, options, and supported workflows. For example, its client can create a workspace:

```python
geOr_api.geoserver.create_workspace("example")
```

This call changes the server and requires an account with appropriate GeoServer permissions.

## Metadata helpers

`Metadata`, `ThesaurusKeyword`, and `Meta_manipulation` are exported by `geOrchestra.meta_apis`.

### `Metadata`

`Metadata(xml_string="")` parses an ISO metadata XML string and discovers its XML namespaces. If parsing fails, `meta` is set to `None`.

| Method | Purpose | Result notes |
| --- | --- | --- |
| `load_from_file(filename_path)` | Load and parse an XML file, then discover its namespaces | Updates the instance; parsing and file errors are raised. |
| `save_into_file(filename_path)` | Write the current XML document to a file | Returns no value. |
| `to_string()` | Serialize the current document as pretty-printed XML | Returns an empty string if no document is loaded. |
| `get_value_xpath(xpath, custom_namespaces=None)` | Evaluate an XPath and serialize the first match | Returns XML text; returns `None` if no match is found. |
| `update_value_xpath(xpath, value="")` | Replace the first XPath match with an XML fragment or plain text | Updates the document in place; prints a message if the path is not found. |
| `add_thesaurus_to_metadata(thesaurus)` | Append a `ThesaurusKeyword` element to the identification section | Updates the document in place. |

`apply_xslt_tranformation`, `search_and_replace`, and `append_value_xpath` are placeholders and currently do nothing.

### `ThesaurusKeyword`

| Member | Purpose |
| --- | --- |
| `ThesaurusKeyword(concept=None, keyword=None, thesaurus_shortlink=None, thesaurus_url=None, thesaurus_title=None, thesaurus_key=None)` | Create a keyword helper with optional concept and thesaurus fields. |
| `load_from_json_get_thesaurus_dict(data)` | Populate thesaurus properties from a GeoNetwork thesaurus response. |
| `load_from_json_search_thesaurus_dict(data)` | Populate the concept, keyword, and thesaurus key from a vocabulary search result. |
| `to_xml()` | Create an ISO 19115-3 descriptive-keyword XML fragment. |
| `tostring()` | Return the helper's values as a comma-separated string. |

### `Meta_manipulation`

| Method | Purpose | Result notes |
| --- | --- | --- |
| `add_thesaurus(metadata, title, server, thesaurus_value, local_thesaurus_name)` | Add legacy ISO 19139 thesaurus XML to a metadata string | Returns the modified metadata string. |
| `transform_metadata_from_geonode_to_gn(...)` | Transform GeoNode metadata for a GeoNetwork migration workflow | Depends on instance attributes not initialized by the constructor; inspect the implementation before use. |
| `transform_feature_from_geonode_to_gn(...)` | Transform GeoNode feature metadata for a GeoNetwork migration workflow | Depends on instance attributes not initialized by the constructor; inspect the implementation before use. |
