from geOrchestra.meta_apis import GN_API
from geOrchestra.console import Console_api



class geOrchestra:
    def __init__(self, server, username, password, verifytls=True, with_geoserver=True):
        self.server = server
        self.username = username
        self.password = password
        self.verifytls = verifytls
        self.gn = GN_API(server, username, password, verifytls=verifytls)
        self.console = Console_api(server, username, password, verifytls=verifytls)
        self.geoserver = None
        if with_geoserver:
            try:
                from geoservercloud import GeoServerCloud
            except ModuleNotFoundError as error:
                if error.name != "geoservercloud":
                    raise
            else:
                self.geoserver = GeoServerCloud(
                    url=server + "/geoserver/",
                    user=username,
                    password=password,
                    verifytls=verifytls,
                )


