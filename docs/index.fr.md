# Bibliothèque Python geOrchestra

`geOrchestra` est un package Python permettant d'automatiser des opérations sur les services geOrchestra. Son client principal regroupe des clients pour GeoNetwork, la Console geOrchestra et GeoServer Cloud.

Le package fait partie de [geo-utils](https://github.com/georchestra/geo-utils), un dépôt d'outils et de scripts d'administration geOrchestra. Ce guide porte uniquement sur la bibliothèque Python.

## Pour commencer

- [Guide utilisateur](user_guide/index.md) : installation, connexion et première requête.
- [Référence de l'API](technical_guides/api_reference.md) : méthodes disponibles et limites importantes.

## Informations sur le projet

- Python : version 3.9 ou ultérieure
- Package : `geOrchestra`
- Dépôt : [georchestra/geo-utils](https://github.com/georchestra/geo-utils)
- Dépendances déclarées : `requests`, `python-dotenv` et `geoservercloud`

La bibliothèque évolue et regroupe des clients de services. Consultez la référence et le code source avant d'utiliser une méthode dans un workflow de production : la gestion des erreurs et les valeurs de retour ne sont pas uniformes.
