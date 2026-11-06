import requests


class MaelstroError(Exception):
    pass


class Maelstro:
    """Client for the geOrchestra Maelstro backend (FastAPI), served under /maelstro-backend."""

    def __init__(self, server, username, password, verifytls=True, root_path="/maelstro-backend"):
        self.server = server.rstrip("/")
        self.root_path = root_path
        self.username = username
        self.password = password
        self.verifytls = verifytls
        self.session = requests.Session()
        self.session.verify = verifytls
        self.session.auth = (username, password)
        self.session.headers.update({"Accept": "application/json"})

    @property
    def base_url(self):
        return self.server + self.root_path

    def _request(self, path, params=None):
        response = self.session.get(self.base_url + path, params=params)
        if response.status_code != 200:
            raise MaelstroError(f"GET {path} failed: {response.status_code} {response.text}")
        return response

    def _get(self, path, params=None):
        return self._request(path, params).json()

    def get_logs(self, size=5, offset=0, get_details=False):
        """Return the history of copy operations (newest first) as a list of JSON records."""
        params = {"size": size, "offset": offset, "get_details": str(get_details).lower()}
        return self._get("/logs", params=params)

    def get_logs_count(self):
        """Return the total number of records in the copy history."""
        response = self._request("/logs", params={"size": 1})
        return int(response.headers["x-total-count"])

    def get_all_logs(self, page_size=50, get_details=False):
        """Iterate over the whole copy history, fetching page by page."""
        offset = 0
        while True:
            page = self.get_logs(page_size, offset, get_details)
            yield from page
            if len(page) < page_size:
                return
            offset += page_size

    def get_sources(self):
        return self._get("/sources")

    def get_destinations(self):
        return self._get("/destinations")

    def copy_preview(self, src_name, dst_name, metadata_uuid,
                     copy_meta=True, copy_layers=True, copy_styles=True):
        """Preview what a copy of a metadata (and its layers/styles) would do, without changing anything."""
        params = {
            "src_name": src_name,
            "dst_name": dst_name,
            "metadataUuid": metadata_uuid,
            "copy_meta": str(copy_meta).lower(),
            "copy_layers": str(copy_layers).lower(),
            "copy_styles": str(copy_styles).lower(),
        }
        return self._get("/copy_preview", params=params)
