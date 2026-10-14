## [Console : `Console_api`](https://github.com/georchestra/geo-utils/blob/main/geOrchestra/console/console.py)

L’attribut `console` du client principal est une instance de `Console_api`. Il envoie des requêtes à `/console/private/...` avec l’authentification HTTP Basic.

### Exemple

Modifier la description d’un utilisateur, puis créer et supprimer un utilisateur et une organisation de test (extrait du bloc `__main__` des sources) :

```python
import json

console = geOr_api.console

user = json.loads(console.getusers(uid="testadmin"))
user["orgObj"] = json.loads(console.getorgs(uid=user["org"]))
user["description"] = "Description modifiée avec l’API"
print(console.updateuserdetails(uid=user["uid"], json=json.dumps(user)))

print(console.createnewuser(org="PSC", sn="testapi", givenname="test",
                            mail="testapi@example.org",
                            description="Cet utilisateur a été créé avec l’API"))
print(console.deluser(id="testapi"))

print(console.createneworgs(name="TESTAPI", shortName="testapi", orgType="Other"))
print(console.delorgs(id="testapi"))
```

### Utilisateurs

| Méthode | Description | Remarques sur le résultat |
| --- | --- | --- |
| `getusers(uid="", filter=None)` | Récupère un utilisateur par UID ou appelle l’endpoint des utilisateurs | Texte de la réponse si HTTP 200 ; sinon `None`. Le paramètre `filter` n’est actuellement pas utilisé. |
| `createnewuser(org, sn, givenname, mail, description)` | Crée un utilisateur | Texte de la réponse si HTTP 200 ; sinon une chaîne d’erreur. |
| `updateuserdetails(uid, json)` | Modifie un utilisateur ; `json` est le corps de requête encodé en JSON | Texte de la réponse si HTTP 200 ; sinon `None`. |
| `deluser(id)` | Supprime un utilisateur | Texte de la réponse si HTTP 200 ; sinon une chaîne d’erreur. |

### Organisations

| Méthode | Description | Remarques sur le résultat |
| --- | --- | --- |
| `getorgs(uid="", filter=None)` | Récupère une organisation par UID ou appelle l’endpoint des organisations | Texte de la réponse si HTTP 200 ; sinon `None`. Le paramètre `filter` n’est actuellement pas utilisé. |
| `createneworgs(name, shortName, orgType, address="", description="", note="", mail="", url="", b64logo="")` | Crée une organisation | `orgType` doit être un type pris en charge par Console, par exemple `Association`, `Company`, `NGO`, `Individual` ou `Other`. Renvoie le texte de la réponse si HTTP 200 ; sinon une chaîne d’erreur. |
| `delorgs(id)` | Supprime une organisation | Texte de la réponse si HTTP 200 ; sinon une chaîne d’erreur. |

### Rôles

| Méthode | Description | Remarques sur le résultat |
| --- | --- | --- |
| `getroles(uid="")` | Récupère les rôles, éventuellement filtrés par `uid` | Texte de la réponse si HTTP 200 ; sinon `None`. |
| `createnewroles(cn="NEWROLE", description="Default description")` | Crée un rôle | Texte de la réponse si HTTP 200 ; sinon une chaîne d’erreur. |
| `updaterolesuser(uuid="testadmin", cn="ROLE")` | Attribue un rôle à un utilisateur | Texte de la réponse si HTTP 200 ; sinon une chaîne d’erreur. |

Ces opérations peuvent nécessiter des privilèges d’administrateur. Les valeurs renvoyées sont du texte de réponse, `None` ou une chaîne d’erreur, et non un type de réponse commun. Vérifiez chaque résultat avant de poursuivre.