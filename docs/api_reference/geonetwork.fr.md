## [GeoNetwork : `GN_API`](https://github.com/georchestra/geo-utils/blob/main/geOrchestra/meta_apis/gn_api.py)

Créez directement le client pour configurer les options propres à GeoNetwork :

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

La vérification des certificats TLS est activée par défaut. `xsrf_via_get=True` utilise `/srv/api/me` ; par défaut, le client utilise l’ancien endpoint `/srv/fre/info?type=me` pour obtenir le cookie XSRF.

### Catalogue et métadonnées

| Méthode | Description | Remarques sur le résultat |
| --- | --- | --- |
| `get_gnversion()` | Récupère les informations du site GeoNetwork et l’identifiant du nœud | Objet JSON analysé |
| `get_all_catalog(steps=100, portal=None)` | Récupère les UUID des fiches du catalogue avec la pagination CSW | Liste d’UUID, ou `None` si aucune fiche ou en cas d’échec de la requête |
| `get_metadataxml(uuid)` | Récupère le document XML d’une fiche | Texte XML si la réponse HTTP est 200 ; sinon `None` |
| `get_metadata_mef_zip(uuid, with_related=True, timeout=120)` | Télécharge une archive MEF ZIP | Octets ZIP si la réponse HTTP est 200 ; sinon `None` |
| `upload_metadata(metadata, groupid="100", uuidprocessing="GENERATEUUID", publish=False)` | Téléverse un objet fichier de métadonnées ; `uuidprocessing` accepte les valeurs GeoNetwork `NOTHING`, `OVERWRITE` et `GENERATEUUID` | JSON analysé en cas de succès ; `False` en cas d’erreur gérée |
| `get_record_privileges(uuid)` | Récupère le groupe propriétaire et la visibilité publique | Dictionnaire en cas de succès ; sinon `None` |

### Thésaurus

| Méthode | Description |
| --- | --- |
| `get_thesaurus_dict(thesaurus_key=None)` | Récupère les informations du thésaurus, éventuellement pour une clé donnée |
| `searchin_thesaurus_dict(keyword="", thesaurus_key=False)` | Recherche des termes, éventuellement limitée à certaines clés de thésaurus |
| `add_thesaurus_dict(filename)` | Téléverse un fichier de thésaurus ; l’implémentation est expérimentale et affiche les détails de la requête |
| `delete_thesaurus_dict(name)` | Supprime un thésaurus par son nom ou sa clé |

### Moissonnage

| Méthode | Description | Remarques sur le résultat |
| --- | --- | --- |
| `get_harvests()` | Liste les configurations de récolte | JSON analysé en cas de succès ; `"Error"` sinon |
| `make_harvest_local(uuid)` | Associe une récolte au nœud GeoNetwork local | `"Okay"` ou `False` ; le délai d’attente peut atteindre une heure |
| `delete_harvest(id)` | Supprime une configuration de récolte | Réponse JSON analysée |

### Sélections de recherche et modifications par lot

| Méthode | Description |
| --- | --- |
| `search_keyword(keywords)` | Recherche des fiches à l’aide de la requête GeoNetwork configurée |
| `get_search_buckets()` | Liste les sélections de recherche enregistrées |
| `get_search_bucket(name)` | Récupère une sélection par son nom |
| `feed_search_bucket(name, uuid)` | Ajoute un ou plusieurs UUID de fiches à une sélection |
| `purge_search_bucket(name, uuid=None)` | Retire les UUID indiqués ou supprime/efface la sélection si aucun UUID n’est fourni |
| `batch_edit_search_and_replace(bucket_name, search, replace, regex_flags="", use_regex="false", update_date_stamp="false")` | Recherche et remplace des valeurs de métadonnées dans les fiches d’une sélection |
| `batch_edit_xpath(bucket_name, xpath, value, update_timestamps=False, action="replace", condition="")` | Applique une modification par lot fondée sur XPath aux fiches d’une sélection |

Les méthodes de modification par lot agissent sur les fiches d’une sélection de recherche. Vérifiez le contenu de la sélection avant d’appliquer des changements. Les réponses JSON sont renvoyées sans gestion d’erreur commune.

Appelez `closesession()` lorsque vous avez terminé avec un client `GN_API` autonome, afin de fermer sa session de requêtes.