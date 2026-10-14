## Outils de métadonnées

`Metadata`, `ThesaurusKeyword` et `Meta_manipulation` sont exportés par `geOrchestra.meta_apis`.

### `Metadata`

`Metadata(xml_string="")` analyse une chaîne XML de métadonnées ISO et détecte ses espaces de noms XML. En cas d’échec de l’analyse, `meta` est défini sur `None`.

| Méthode | Description | Remarques sur le résultat |
| --- | --- | --- |
| `load_from_file(filename_path)` | Charge et analyse un fichier XML, puis détecte ses espaces de noms | Met à jour l’instance ; les erreurs d’analyse et de fichier sont levées. |
| `save_into_file(filename_path)` | Écrit le document XML courant dans un fichier | Ne renvoie aucune valeur. |
| `to_string()` | Sérialise le document courant en XML mis en forme | Renvoie une chaîne vide si aucun document n’est chargé. |
| `get_value_xpath(xpath, custom_namespaces=None)` | Évalue une expression XPath et sérialise le premier résultat | Renvoie du texte XML ; renvoie `None` si aucun résultat n’est trouvé. |
| `update_value_xpath(xpath, value="")` | Remplace le premier résultat XPath par un fragment XML ou du texte brut | Met à jour le document sur place ; affiche un message si le chemin n’est pas trouvé. |
| `add_thesaurus_to_metadata(thesaurus)` | Ajoute un élément `ThesaurusKeyword` à la section d’identification | Met à jour le document sur place. |

`apply_xslt_tranformation`, `search_and_replace` et `append_value_xpath` sont des méthodes provisoires qui ne font actuellement rien.

### `ThesaurusKeyword`

| Membre | Description |
| --- | --- |
| `ThesaurusKeyword(concept=None, keyword=None, thesaurus_shortlink=None, thesaurus_url=None, thesaurus_title=None, thesaurus_key=None)` | Crée un objet utilitaire de mots-clés avec des champs de concept et de thésaurus facultatifs. |
| `load_from_json_get_thesaurus_dict(data)` | Renseigne les propriétés du thésaurus à partir d’une réponse de thésaurus GeoNetwork. |
| `load_from_json_search_thesaurus_dict(data)` | Renseigne le concept, le mot-clé et la clé du thésaurus à partir d’un résultat de recherche dans un vocabulaire. |
| `to_xml()` | Crée un fragment XML de mots-clés descriptifs ISO 19115-3. |
| `tostring()` | Renvoie les valeurs de l’objet sous forme de chaîne séparée par des virgules. |

### `Meta_manipulation`

| Méthode | Description | Remarques sur le résultat |
| --- | --- | --- |
| `add_thesaurus(metadata, title, server, thesaurus_value, local_thesaurus_name)` | Ajoute à une chaîne de métadonnées du XML de thésaurus au format ISO 19139 hérité | Renvoie la chaîne de métadonnées modifiée. |
| `transform_metadata_from_geonode_to_gn(...)` | Transforme des métadonnées GeoNode dans le cadre d’une migration vers GeoNetwork | Dépend d’attributs d’instance non initialisés par le constructeur ; consultez l’implémentation avant utilisation. |
| `transform_feature_from_geonode_to_gn(...)` | Transforme les métadonnées d’une entité GeoNode dans le cadre d’une migration vers GeoNetwork | Dépend d’attributs d’instance non initialisés par le constructeur ; consultez l’implémentation avant utilisation. |