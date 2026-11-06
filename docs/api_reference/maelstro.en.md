## [Maelstro: `Maelstro`](https://github.com/georchestra/geo_utils/blob/main/geOrchestra/maelstro.py#L8)

The top-level client's `maelstro` attribute is an instance of `Maelstro`. It sends requests to the [Maelstro](https://github.com/georchestra/maelstro) backend (`/maelstro-backend/...`) using HTTP Basic authentication. Maelstro synchronises GeoNetwork metadata and GeoServer layers between instances.

### Example

Preview the copy of a dataset from a source to a destination, without changing anything:

```python
maelstro = geOr_api.maelstro

print(maelstro.get_sources())
print(maelstro.get_destinations())

preview = maelstro.copy_preview(
    src_name="my_source",
    dst_name="my_destination",
    metadata_uuid="00000000-0000-0000-0000-000000000000",
    copy_layers=True,
    copy_styles=False,
)
print(preview)
```

### Methods

| Method | Purpose | Result notes |
| --- | --- | --- |
| `get_sources()` | List the GeoNetwork sources configured in Maelstro (`GET /sources`) | Parsed JSON. |
| `get_destinations()` | List the GeoNetwork/GeoServer destinations configured in Maelstro (`GET /destinations`) | Parsed JSON. |
| `copy_preview(src_name, dst_name, metadata_uuid, copy_meta=True, copy_layers=True, copy_styles=True)` | Preview a copy of a metadata record and its linked layers and styles (`GET /copy_preview`) | Parsed JSON. Nothing is modified. |

Unlike `Console_api`, a response other than HTTP 200 raises `MaelstroError` with the status code and response text. The actual copy (`PUT /copy`) is not yet supported.

### History

| Method | Purpose | Result notes |
| --- | --- | --- |
| `get_logs(size=5, offset=0, get_details=False)` | Read copy history records, newest first (`GET /logs`) | List of JSON records. With `get_details=True`, each record also contains the elementary operations (API calls). |
| `get_logs_count()` | Total number of history records (`x-total-count` header) | `int`. |
| `get_all_logs(page_size=50, get_details=False)` | Iterate over the whole history, page by page | Generator of JSON records. |

The history requires database logging to be configured in Maelstro; otherwise the server answers HTTP 500 ("DB logging not configured") and `MaelstroError` is raised.

```python
print(maelstro.get_logs_count())
for record in maelstro.get_logs(size=10, get_details=True):
    print(record)
```
