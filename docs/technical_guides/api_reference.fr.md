# Référence de l'API

Le package expose actuellement les imports suivants :

```python
from geOrchestra import geOrchestra
from geOrchestra.console import Console_api
from geOrchestra.meta_apis import GN_API, Meta_manipulation, Metadata, ThesaurusKeyword
```

`geOrchestra` est également exporté par le package racine. L'API est un wrapper léger autour de points d'accès HTTP, et non un client typé avec des réponses normalisées : les valeurs de retour et la gestion des erreurs varient selon les méthodes.

## Client principal

```python
geOr_api = geOrchestra(server, username, password)
```

`server` est l'URL de base de l'instance, sans barre oblique finale. Le client fournit les attributs suivants :

| Attribut | Client | Rôle |
| --- | --- | --- |
| `geOr_api.gn` | `GN_API` | API GeoNetwork de catalogue et de métadonnées |
| `geOr_api.console` | `Console_api` | API Console pour les utilisateurs, organisations et rôles |
| `geOr_api.geoserver` | `GeoServerCloud` | Client fourni par la dépendance GeoServer Cloud |

L'initialisation crée immédiatement les trois clients de service. Le client GeoNetwork effectue des requêtes pour lire les informations du site et obtenir un cookie XSRF. Le constructeur principal n'accepte pas d'options de configuration supplémentaires.

## GeoNetwork : `GN_API`

Instanciez directement le client pour configurer les options propres à GeoNetwork :

```python
from geOrchestra.meta_apis import GN_API

gn = GN_API(
    server,
    username,
    password,
    verifytls=True,
    prefix_gn_url="/geonetwork",
    xsrf_via_get=False,
)
```

La vérification du certificat TLS est activée par défaut. `xsrf_via_get=True` utilise `/srv/api/me` ; par défaut, le client utilise l'ancien point d'accès `/srv/fre/info?type=me` pour obtenir le cookie XSRF.

### Catalogue et métadonnées

| Méthode | Rôle | Résultat |
| --- | --- | --- |
| `get_gnversion()` | Lire les informations du site GeoNetwork et l'identifiant du nœud | Objet JSON analysé |
| `get_all_catalog(steps=100, portal=None)` | Récupérer les UUID des fiches du catalogue par pagination CSW | Liste d'UUID, ou `None` si aucune fiche ou en cas d'échec de requête |
| `get_metadataxml(uuid)` | Lire le document XML d'une fiche | Texte XML si le statut HTTP vaut 200 ; sinon `None` |
| `get_metadata_mef_zip(uuid, with_related=True, timeout=120)` | Télécharger une archive MEF ZIP | Octets ZIP si le statut HTTP vaut 200 ; sinon `None` |
| `upload_metadata(metadata, groupid="100", uuidprocessing="GENERATEUUID", publish=False)` | Importer un objet fichier de métadonnées | JSON analysé en cas de succès ; `False` pour les échecs pris en charge |
| `get_record_privileges(uuid)` | Lire le groupe propriétaire et la visibilité publique d'une fiche | Dictionnaire en cas de succès ; sinon `None` |

`uuidprocessing` accepte les valeurs GeoNetwork `NOTHING`, `OVERWRITE` et `GENERATEUUID`. Le mode `OVERWRITE` peut remplacer une fiche existante : vérifiez l'UUID et les autorisations avant utilisation.

### Thésaurus

| Méthode | Rôle |
| --- | --- |
| `get_thesaurus_dict(thesaurus_key=None)` | Récupérer les informations d'un ou de plusieurs thésaurus |
| `searchin_thesaurus_dict(keyword="", thesaurus_key=False)` | Rechercher des termes, éventuellement dans certains thésaurus |
| `add_thesaurus_dict(filename)` | Importer un fichier de thésaurus ; cette méthode est expérimentale et affiche des détails de requête |
| `delete_thesaurus_dict(name)` | Supprimer un thésaurus à partir de son nom ou de sa clé |

### Moissonneurs

| Méthode | Rôle | Résultat |
| --- | --- | --- |
| `get_harvests()` | Lister les configurations de moissonnage | JSON analysé en cas de succès ; `"Error"` sinon |
| `make_harvest_local(uuid)` | Affecter un moissonneur au nœud GeoNetwork local | `"Okay"` ou `False` ; délai d'attente pouvant atteindre une heure |
| `delete_harvest(id)` | Supprimer une configuration de moissonnage | Réponse JSON analysée |

### Sélections de recherche et modifications par lots

| Méthode | Rôle |
| --- | --- |
| `search_keyword(keywords)` | Rechercher des fiches avec la requête GeoNetwork configurée |
| `get_search_buckets()` | Lister les sélections de recherche enregistrées |
| `get_search_bucket(name)` | Lire une sélection par son nom |
| `feed_search_bucket(name, uuid)` | Ajouter un ou plusieurs UUID de fiches à une sélection |
| `purge_search_bucket(name, uuid=None)` | Retirer les UUID indiqués ou, sans UUID, supprimer la sélection |
| `batch_edit_search_and_replace(bucket_name, search, replace, regex_flags="", use_regex="false", update_date_stamp="false")` | Rechercher et remplacer des valeurs de métadonnées pour les fiches d'une sélection |
| `batch_edit_xpath(bucket_name, xpath, value, update_timestamps=False, action="replace", condition="")` | Appliquer une modification XPath aux fiches d'une sélection |

Les modifications par lots s'appliquent aux fiches d'une sélection. Vérifiez son contenu avant toute modification. Les réponses JSON sont renvoyées sans mécanisme commun de gestion des erreurs.

Appelez `closesession()` à la fin de l'utilisation d'un client `GN_API` autonome pour fermer sa session HTTP.

## Console : `Console_api`

L'attribut `console` du client principal est une instance de `Console_api`. Les requêtes sont envoyées aux points d'accès `/console/private/...` avec une authentification HTTP Basic.

### Utilisateurs

| Méthode | Rôle | Résultat |
| --- | --- | --- |
| `getusers(uid="", filter=None)` | Lire un utilisateur par UID ou appeler le point d'accès de liste | Texte de réponse si le statut HTTP vaut 200 ; sinon `None`. Le paramètre `filter` n'est pas utilisé actuellement. |
| `createnewuser(org, sn, givenname, mail, description)` | Créer un utilisateur | Texte de réponse si le statut HTTP vaut 200 ; sinon une chaîne d'erreur. |
| `updateuserdetails(uid, json)` | Modifier un utilisateur ; `json` doit être un corps de requête encodé en JSON | Texte de réponse si le statut HTTP vaut 200 ; sinon `None`. |
| `deluser(id)` | Supprimer un utilisateur | Texte de réponse si le statut HTTP vaut 200 ; sinon une chaîne d'erreur. |

### Organisations

| Méthode | Rôle | Résultat |
| --- | --- | --- |
| `getorgs(uid="", filter=None)` | Lire une organisation par UID ou appeler le point d'accès de liste | Texte de réponse si le statut HTTP vaut 200 ; sinon `None`. Le paramètre `filter` n'est pas utilisé actuellement. |
| `createneworgs(name, shortName, orgType, address="", description="", note="", mail="", url="", b64logo="")` | Créer une organisation | `orgType` doit correspondre à un type accepté par la Console, par exemple `Association`, `Company`, `NGO`, `Individual` ou `Other`. Texte de réponse si le statut HTTP vaut 200 ; sinon une chaîne d'erreur. |
| `delorgs(id)` | Supprimer une organisation | Texte de réponse si le statut HTTP vaut 200 ; sinon une chaîne d'erreur. |

### Rôles

| Méthode | Rôle | Résultat |
| --- | --- | --- |
| `getroles(uid="")` | Lire les rôles, éventuellement pour un `uid` donné | Texte de réponse si le statut HTTP vaut 200 ; sinon `None`. |
| `createnewroles(cn="NEWROLE", description="Default description")` | Créer un rôle | Texte de réponse si le statut HTTP vaut 200 ; sinon une chaîne d'erreur. |
| `updaterolesuser(uuid="testadmin", cn="ROLE")` | Attribuer un rôle à un utilisateur | Texte de réponse si le statut HTTP vaut 200 ; sinon une chaîne d'erreur. |

Ces opérations peuvent nécessiter des privilèges d'administration. Les valeurs de retour sont du texte de réponse, `None` ou une chaîne d'erreur, sans type commun. Vérifiez le résultat de chaque appel avant de poursuivre.

## GeoServer Cloud

L'attribut `geoserver` du client principal est une instance `GeoServerCloud` fournie par la [bibliothèque Python GeoServer Cloud](https://github.com/camptocamp/python-geoservercloud). Le wrapper la configure avec le chemin `/geoserver/` de l'instance et les identifiants fournis.

Consultez la [documentation de la bibliothèque GeoServer Cloud](https://camptocamp.github.io/python-geoservercloud/) pour connaître ses méthodes, options et cas d'utilisation. Par exemple, son client peut créer un espace de travail :

```python
geOr_api.geoserver.create_workspace("example")
```

Cet appel modifie le serveur et nécessite un compte disposant des autorisations GeoServer adéquates.

## Outils de métadonnées

`Metadata`, `ThesaurusKeyword` et `Meta_manipulation` sont exportés par `geOrchestra.meta_apis`.

### `Metadata`

`Metadata(xml_string="")` analyse une chaîne XML de métadonnées et détecte ses espaces de noms. En cas d'échec de l'analyse, `meta` vaut `None`.

| Méthode | Rôle | Résultat |
| --- | --- | --- |
| `load_from_file(filename_path)` | Charger et analyser un fichier XML, puis détecter ses espaces de noms | Modifie l'instance ; les erreurs de fichier ou d'analyse sont levées. |
| `save_into_file(filename_path)` | Écrire le document XML courant dans un fichier | Ne renvoie aucune valeur. |
| `to_string()` | Sérialiser le document courant en XML indenté | Renvoie une chaîne vide si aucun document n'est chargé. |
| `get_value_xpath(xpath, custom_namespaces=None)` | Évaluer un XPath et sérialiser le premier résultat | Renvoie le texte XML ou `None` si aucun élément ne correspond. |
| `update_value_xpath(xpath, value="")` | Remplacer le premier résultat XPath par un fragment XML ou du texte | Modifie le document en place ; affiche un message si le chemin est introuvable. |
| `add_thesaurus_to_metadata(thesaurus)` | Ajouter un élément `ThesaurusKeyword` à la section d'identification | Modifie le document en place. |

`apply_xslt_tranformation`, `search_and_replace` et `append_value_xpath` sont des méthodes provisoires qui ne font actuellement rien.

### `ThesaurusKeyword`

| Membre | Rôle |
| --- | --- |
| `ThesaurusKeyword(concept=None, keyword=None, thesaurus_shortlink=None, thesaurus_url=None, thesaurus_title=None, thesaurus_key=None)` | Créer un objet avec des champs facultatifs pour le concept et le thésaurus. |
| `load_from_json_get_thesaurus_dict(data)` | Charger les propriétés du thésaurus depuis une réponse GeoNetwork. |
| `load_from_json_search_thesaurus_dict(data)` | Charger le concept, le terme et la clé du thésaurus depuis un résultat de recherche. |
| `to_xml()` | Créer un fragment XML de mot-clé descriptif ISO 19115-3. |
| `tostring()` | Renvoyer les valeurs de l'objet sous forme de chaîne séparée par des virgules. |

### `Meta_manipulation`

| Méthode | Rôle | Résultat |
| --- | --- | --- |
| `add_thesaurus(metadata, title, server, thesaurus_value, local_thesaurus_name)` | Ajouter un fragment de thésaurus ISO 19139 historique à une chaîne de métadonnées | Renvoie la chaîne de métadonnées modifiée. |
| `transform_metadata_from_geonode_to_gn(...)` | Transformer des métadonnées GeoNode pour une migration vers GeoNetwork | Dépend d'attributs d'instance qui ne sont pas initialisés par le constructeur ; inspectez le code avant utilisation. |
| `transform_feature_from_geonode_to_gn(...)` | Transformer des métadonnées d'entité GeoNode pour une migration vers GeoNetwork | Dépend d'attributs d'instance qui ne sont pas initialisés par le constructeur ; inspectez le code avant utilisation. |
