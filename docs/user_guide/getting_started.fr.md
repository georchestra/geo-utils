# Prise en main

## Prérequis

- Python 3.9 ou ultérieur
- Une instance geOrchestra accessible depuis la machine qui exécute le script
- Un nom d'utilisateur et un mot de passe autorisés à accéder aux services et à effectuer les opérations nécessaires

## Installation

Installez le package directement depuis GitHub :

```bash
python -m pip install "git+https://github.com/georchestra/geo-utils.git"
```

Les métadonnées du package déclarent les dépendances `requests`, `python-dotenv` et `geoservercloud`. Si Python est géré par le système d'exploitation, utilisez plutôt un environnement virtuel que de contourner ses protections d'installation.

## Connexion

Indiquez l'URL de base de l'instance geOrchestra sans barre oblique finale. Le client utilise les identifiants fournis pour les requêtes aux services. Ne stockez pas les identifiants dans le dépôt ; cet exemple les lit dans des variables d'environnement.

```python
import json
import os
from geOrchestra import geOrchestra

server = os.environ["GEORCHESTRA_URL"].rstrip("/")
username = os.environ["GEORCHESTRA_USERNAME"]
password = os.environ["GEORCHESTRA_PASSWORD"]

geOr_api = geOrchestra(server, username, password)

# GeoNetwork : récupérer les identifiants des fiches et le XML d'une fiche
record_ids = geOr_api.gn.get_all_catalog(steps=50)
print(f"Fiches du catalogue : {len(record_ids or [])}")
if record_ids:
    metadata_xml = geOr_api.gn.get_metadataxml(record_ids[0])

# Console : lire un utilisateur ; la méthode renvoie du texte JSON en cas de succès
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

Tous les services sont accessibles depuis la même instance `geOr_api`. Ses attributs sont des clients de services distincts, pas une API unifiée : GeoNetwork, la Console et GeoServer Cloud ont chacun leurs propres noms de méthodes et types de retour.

### Utiliser le client GeoServer Cloud

Le wrapper crée `geOr_api.geoserver` avec la même URL d'instance et les mêmes identifiants. Ses méthodes sont fournies par la [bibliothèque Python GeoServer Cloud](https://github.com/camptocamp/python-geoservercloud). Par exemple, pour créer un espace de travail :

```python
geOr_api.geoserver.create_workspace("example")
```

Cet appel modifie le serveur. Choisissez un nom d'espace de travail adapté à votre environnement et utilisez un compte autorisé à administrer GeoServer. La [documentation amont](https://camptocamp.github.io/python-geoservercloud/) décrit les autres méthodes.

### Effectuer une modification dans la Console

Les méthodes de la Console sont également accessibles depuis le wrapper. Cet exemple crée un utilisateur dans une organisation existante :

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

Cet appel crée réellement un compte dans la Console. Vérifiez que l'organisation existe et que les identifiants disposent des autorisations nécessaires avant de l'exécuter.

Définissez les variables d'environnement avant de lancer le script :

```bash
export GEORCHESTRA_URL="https://demo.georchestra.org"
export GEORCHESTRA_USERNAME="your-user"
export GEORCHESTRA_PASSWORD="your-password"
python your_script.py
```

## Détails de connexion

La création de `geOrchestra(...)` instancie les clients GeoNetwork, Console et GeoServer Cloud. L'initialisation de GeoNetwork effectue des requêtes HTTP pour lire les informations du site et obtenir un cookie XSRF. La création du client nécessite donc un accès réseau et un point d'accès GeoNetwork fonctionnel. Le chemin GeoNetwork utilisé par défaut est `/geonetwork`.

La vérification des certificats TLS est activée par défaut pour GeoNetwork. Ne définissez `verifytls` à `False` que dans un environnement de test contrôlé, en cas de problème connu de certificat ; désactiver la vérification réduit la sécurité de la connexion. Le constructeur principal n'expose pas les options GeoNetwork : instanciez directement `GN_API` uniquement si vous devez configurer son chemin ou sa vérification TLS.

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

## Vérifier les résultats

Les valeurs de retour dépendent de la méthode. Certaines requêtes réussies renvoient des objets Python issus du JSON, d'autres du texte de réponse. En cas d'échec, une méthode peut renvoyer `None`, `False` ou une chaîne d'erreur. Plusieurs méthodes ne vérifient pas les réponses HTTP négatives. Vérifiez et validez le résultat avant de l'utiliser dans une automatisation ou une opération destructive.

Les méthodes de la Console peuvent créer, modifier et supprimer des utilisateurs, des organisations et des affectations de rôles. Les méthodes GeoNetwork peuvent importer ou modifier des métadonnées et la configuration des moissonneurs. Utilisez un compte avec le minimum de privilèges nécessaires, testez d'abord sur une instance hors production et vérifiez les identifiants ciblés avant toute modification.
