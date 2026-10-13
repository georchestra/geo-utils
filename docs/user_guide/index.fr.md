# Guide utilisateur

Ce guide s'adresse aux scripts Python qui appellent les services geOrchestra avec un compte autorisé à effectuer les opérations demandées.

## Clients disponibles

Le client `geOrchestra` expose trois attributs :

- `geOr_api.gn` pour les opérations de catalogue et de métadonnées GeoNetwork.
- `geOr_api.console` pour les utilisateurs, organisations et rôles de la Console.
- `geOr_api.geoserver` pour le [client Python GeoServer Cloud](https://github.com/camptocamp/python-geoservercloud).

Les deux premiers clients sont implémentés dans ce dépôt. Le comportement du client GeoServer Cloud est fourni par sa dépendance externe.

Consultez le guide [Prise en main](getting_started.md) pour installer le package et effectuer une première requête.
