from geoservercloud import GeoServerCloud
from geOrchestra.meta_apis import GN_API
from geOrchestra.console import Console_api
from geOrchestra.maelstro import Maelstro



class geOrchestra:
    def __init__(self, server, username, password, verifytls=True):
        self.server = server
        self.username = username
        self.password = password
        self.verifytls = verifytls
        self.gn = GN_API(server, username, password, verifytls=verifytls)
        self.console = Console_api(server, username, password, verifytls=verifytls)
        self.maelstro = Maelstro(server, username, password, verifytls=verifytls)
        self.geoserver = GeoServerCloud(
            url=server + "/geoserver/",
            user=username,
            password=password,
            verifytls=verifytls,
        )


