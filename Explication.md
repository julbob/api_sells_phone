### Choix du type de base de données

## MongoDB vs SQL

Etant donné que le client, nous fournit un exemple en csv et donc de forme rectangulaire, l'utilisation de MongoDB ne me semblait pas pertinente. Je suis donc parti sur une base de données SQL.

## PostGreSQL

Possibilité : Microsoft SQL, Oracle, SQLite, MySQL, PostGreSQL

J'ai exclus les solutions Microsoft SQL et Oracle pour rester sur des bases open source et sans license.
J'ai préféré éviter SQLite pour ne pas être rapidement limité.
J'ai choisi PostGreSQL plutôt que MySQL car PostGreSQL semble être de meilleures qualité.

### Développement Python

Possibilité :
- Database: Django ORM, SQLAlchemy, psycopg2
- Web: Flask, FastAPI, Django

## Rejet de Django

J'ai préféré ne pas utilisé Django car le framework me parraissait trop complexe pour un système qui semble relativement simple (API + DB, pas de page, formulaire ect...). Django est aussi connu pour être moins performant que des micro framework comme Flask ou FastAPI bien que plus sécurisé

## Choix de Flask

J'ai préféré utilisé Flask plutôt que FastAPI car je suis plus habitué à ce framework que FastAPI. La communauté de Flask me semble aussi plus importante ce qui peut permettre de trouver des solutions plus facilement. Ils semblent relativement similaires en termes de performances

## Choix de SQLAlchemy

J'ai préféré partir sur SQLAlchemy après avoir rejeter Django pour garder une librairie avec un système d'ORM ce qui permet une gestion plus simple pour intéragir entre le code Python et SQL et d'éviter certains problèmes de sécurité en passant par psycopg2 ou d'autres librairies qui demanderait d'exécuter des commandes SQL dynamique qui pourrait être sensible à une injection SQL ou d'autres failles.
