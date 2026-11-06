## [Maelstro : `Maelstro`](https://github.com/georchestra/geo_utils/blob/main/geOrchestra/maelstro.py#L8)

L’attribut `maelstro` du client principal est une instance de `Maelstro`. Il envoie des requêtes au backend [Maelstro](https://github.com/georchestra/maelstro) (`/maelstro-backend/...`) avec l’authentification HTTP Basic. Maelstro synchronise des métadonnées GeoNetwork et des couches GeoServer entre instances.

### Exemple

Prévisualiser la copie d’un jeu de données d’une source vers une destination, sans rien modifier :

```python
maelstro = geOr_api.maelstro

print(maelstro.get_sources())
print(maelstro.get_destinations())

preview = maelstro.copy_preview(
    src_name="ma_source",
    dst_name="ma_destination",
    metadata_uuid="00000000-0000-0000-0000-000000000000",
    copy_layers=True,
    copy_styles=False,
)
print(preview)
```

### Méthodes

| Méthode | Description | Remarques sur le résultat |
| --- | --- | --- |
| `get_sources()` | Liste les sources GeoNetwork configurées dans Maelstro (`GET /sources`) | JSON décodé. |
| `get_destinations()` | Liste les destinations GeoNetwork/GeoServer configurées dans Maelstro (`GET /destinations`) | JSON décodé. |
| `copy_preview(src_name, dst_name, metadata_uuid, copy_meta=True, copy_layers=True, copy_styles=True)` | Prévisualise la copie d’une fiche de métadonnées et de ses couches et styles liés (`GET /copy_preview`) | JSON décodé. Rien n’est modifié. |

Contrairement à `Console_api`, une réponse autre que HTTP 200 lève `MaelstroError` avec le code de statut et le texte de la réponse. La copie effective (`PUT /copy`) n’est pas encore prise en charge.

### Historique

| Méthode | Description | Remarques sur le résultat |
| --- | --- | --- |
| `get_logs(size=5, offset=0, get_details=False)` | Lit les enregistrements de l’historique des copies, du plus récent au plus ancien (`GET /logs`) | Liste d’enregistrements JSON. Avec `get_details=True`, chaque enregistrement contient aussi les opérations élémentaires (appels d’API). |
| `get_logs_count()` | Nombre total d’enregistrements de l’historique (en-tête `x-total-count`) | `int`. |
| `get_all_logs(page_size=50, get_details=False)` | Parcourt tout l’historique, page par page | Générateur d’enregistrements JSON. |

L’historique nécessite que la journalisation en base de données soit configurée dans Maelstro ; sinon le serveur répond HTTP 500 (« DB logging not configured ») et `MaelstroError` est levée.

```python
print(maelstro.get_logs_count())
for record in maelstro.get_logs(size=10, get_details=True):
    print(record)
```
