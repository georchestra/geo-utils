# Bibliothèque Python geOrchestra

`geOrchestra` est un package Python permettant d’interagir avec les services geOrchestra par script et d’automatiser de nombreuses tâches d’administration de la plateforme de données. Il prend en charge les automatisations GeoNetwork, Console et GeoServer.

Ce package fait partie de [geo-utils](https://github.com/georchestra/geo-utils), un dépôt d’utilitaires et de scripts d’administration geOrchestra. Ce guide porte uniquement sur la bibliothèque Python.

## Documentation de l’API

- [Référence de l’API](api_reference.md) : méthodes des services disponibles et principales limitations.

## Premiers pas

## Prérequis

- Python 3.9 ou version ultérieure
- Une instance geOrchestra accessible depuis la machine qui exécute votre script (par exemple, https://demo.georchestra.org/)
- Un nom d’utilisateur et un mot de passe disposant des autorisations nécessaires pour les services et opérations utilisés

## Installation

Installez le package directement depuis GitHub :

```bash
python3 -m pip install "git+https://github.com/georchestra/geo-utils.git"
```

Les métadonnées du package déclarent `requests`, `python-dotenv` et `geoservercloud` comme dépendances. Si vous installez le package dans un environnement Python système géré de l’extérieur, utilisez un environnement virtuel :

```bash
python3 -m venv venv
source venv/bin/activate
python3 -m pip install "git+https://github.com/georchestra/geo-utils.git"
```

## Exemples

Pour commencer :

```python
import json
import os
from geOrchestra import geOrchestra

server = "https://demo.georchestra.org"
username = "testadmin"
password = "testadmin"

geOr_api = geOrchestra(server, username, password)

# GeoNetwork : récupérer les identifiants des fiches et télécharger un document XML de métadonnées
record_ids = geOr_api.gn.get_all_catalog(steps=50)
print(f"Nombre de fiches dans le catalogue : {len(record_ids or [])}")
if record_ids:
    metadata_xml = geOr_api.gn.get_metadataxml(record_ids[0])

# Console : lire un utilisateur ; les méthodes Console renvoient du texte JSON en cas de succès
user_json = geOr_api.console.getusers(uid=username)
if user_json:
    user = json.loads(user_json)
    print(user.get("uid"), user.get("org"))

# Console : lister les rôles (également renvoyés sous forme de texte JSON)
roles_json = geOr_api.console.getroles()
if roles_json:
    roles = json.loads(roles_json)
    print(roles)
```

Tous les services sont accessibles depuis la même instance `geOr_api`.

### GeoServer

Le wrapper crée `geOr_api.geoserver` en utilisant la même URL d’instance et les mêmes identifiants. Ses méthodes sont fournies par la [bibliothèque Python GeoServer Cloud](https://github.com/camptocamp/python-geoservercloud). Par exemple, pour créer un espace de travail :

```python
geOr_api.geoserver.create_workspace("example")
```

Consultez la [documentation de la bibliothèque](https://camptocamp.github.io/python-geoservercloud/) pour découvrir ses autres méthodes.

### Console

Les méthodes Console sont également accessibles directement depuis le wrapper. Par exemple, pour créer un utilisateur dans une organisation existante :

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

## Détails de connexion

À des fins de développement, vous pouvez désactiver la vérification TLS et personnaliser le préfixe de l’URL GeoNetwork :

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

## Pour aller plus loin

[Référence de l’API](api_reference.md) : méthodes des services disponibles et principales limitations.
