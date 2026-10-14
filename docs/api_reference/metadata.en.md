
## Metadata helpers

`Metadata`, `ThesaurusKeyword`, and `Meta_manipulation` are exported by `geOrchestra.meta_apis`.

### Example

Add a thesaurus keyword found in GeoNetwork to an ISO 19115-3 file and change its identifier (from the `__main__` block of the sources):

```python
from geOrchestra.meta_apis import GN_API, Metadata, ThesaurusKeyword

gn = GN_API("http://localhost:8080", "testadmin", "testadmin")
thesaurus = gn.get_thesaurus_dict("local.theme.geographie-ofb")
keyword = gn.searchin_thesaurus_dict(keyword="Mayotte")[0]

meta = Metadata()
meta.load_from_file("./sample_meta2.xml")

t = ThesaurusKeyword()
t.load_from_json_get_thesaurus_dict(thesaurus)
t.load_from_json_search_thesaurus_dict(keyword)
meta.add_thesaurus_to_metadata(t)

meta.update_value_xpath(
    xpath="/mdb:MD_Metadata/mdb:identificationInfo/mri:MD_DataIdentification"
    "/mri:citation/cit:CI_Citation/cit:identifier/mcc:MD_Identifier/mcc:code"
    "/gco:CharacterString",
    value="testnewidentifier",
)
meta.save_into_file("./sample_meta3.xml")
```

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
