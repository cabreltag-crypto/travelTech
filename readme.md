# Travel Recommender System

## Auteur
Cabrel Tagwouo

## Objectif du projet
Ce projet vise à développer une application web permettant de recommander des destinations de voyage personnalisées à un utilisateur, en se basant sur ses préférences et les caractéristiques des destinations. L’objectif est de fournir des recommandations pertinentes pour chaque utilisateur, tout en offrant des fonctionnalités de profilage et d’analyse des destinations.

## Méthodologie

L’application utilise des méthodes d’apprentissage automatique supervisées et non supervisées :

- **K-Nearest Neighbors (KNN)** :
  - Pour générer des recommandations personnalisées en comparant le profil de l’utilisateur aux destinations existantes.
  - Pour trouver les destinations similaires à une destination donnée.

- **K-Means Clustering** :
  - Pour regrouper les destinations en clusters selon leurs caractéristiques et leurs profils.

Le système prend en compte des critères tels que le budget, la température moyenne, le niveau de sécurité, et les préférences pour différentes activités (plage, montagne, culture, aventure, etc.).

## Authentification

L’application utilise **JWT (JSON Web Token)** via Django REST Framework SimpleJWT pour sécuriser les endpoints.

- **Endpoints publics** :
  - Inscription (`/api/auth/register/`)
  - Connexion (`/api/auth/login/`)
  - Rafraîchissement de token (`/api/auth/refresh/`)

- **Endpoints privés (requièrent JWT access token)** :
  - Générer des recommandations
  - Consulter les destinations similaires
  - Analyser les clusters
  - Créer ou mettre à jour les préférences
  - Consulter le profil voyageur

## Endpoints disponibles

### Authentification

| Méthode | URL | Description |
|---------|-----|-------------|
| POST | /api/auth/register/ | Crée un nouvel utilisateur et renvoie les tokens JWT |
| POST | /api/auth/login/ | Connexion et récupération des tokens JWT |
| POST | /api/auth/refresh/ | Rafraîchit le token d’accès en utilisant le refresh token |
| GET | /api/auth/me/ | Retourne les informations de l’utilisateur connecté |

### Préférences utilisateur

| Méthode | URL | Description |
|---------|-----|-------------|
| POST | /api/users/preferences/ | Crée ou met à jour les préférences de l’utilisateur connecté |

### Recommandations

| Méthode | URL | Description |
|---------|-----|-------------|
| POST | /api/recommendations/generate/ | Génère des recommandations personnalisées pour l’utilisateur connecté. Si aucune recommandation, retourne les destinations les plus populaires. |
| GET | /api/destinations/similar/<id>/ | Retourne les destinations similaires à une destination donnée. |
| POST | /api/destinations/cluster/ | Retourne l’analyse des clusters de destinations basés sur KMeans. |
| GET | /api/users/<id>/travel-profile/ | Retourne le profil voyageur d’un utilisateur, avec un résumé incluant l’intérêt principal, la catégorie de budget, le climat préféré, les activités et les préférences brutes. |

## Guide d’utilisation

### Installation

1. Cloner le projet depuis le dépôt :

```bash
git clone <url_du_projet>
cd travel_recommender
```

2. Créer un environnement virtuel et l’activer :

```bash
python -m venv venv
source venv/bin/activate      # Linux / Mac
venv\Scripts\activate         # Windows
```

3. Installer les dépendances :

```bash
pip install -r requirements.txt
```

4. Appliquer les migrations :

```bash
python manage.py migrate
```

5. Créer un super utilisateur pour accéder à l’admin (optionnel) :

```bash
python manage.py createsuperuser
```

6. Lancer le serveur de développement :

```bash
python manage.py runserver
```

### Utilisation avec Postman

1. **Inscription d’un utilisateur** :
   - POST `/api/auth/register/` avec body JSON `{ "username": "...", "email": "...", "password": "...", "password2": "..." }`

2. **Connexion** :
   - POST `/api/auth/login/` avec body JSON `{ "username": "...", "password": "..." }`
   - Récupérer `access` et `refresh` tokens

3. **Rafraîchir le token** :
   - POST `/api/auth/refresh/` avec body JSON `{ "refresh": "<refresh_token>" }`

4. **Créer / Mettre à jour les préférences** :
   - POST `/api/users/preferences/` avec body JSON contenant les champs de préférences (budget, activités, sécurité, etc.)

5. **Générer des recommandations** :
   - POST `/api/recommendations/generate/` avec `Authorization: Bearer <access_token>`

6. **Destinations similaires** :
   - GET `/api/destinations/similar/<destination_id>/` avec `Authorization: Bearer <access_token>`

7. **Clusters des destinations** :
   - POST `/api/destinations/cluster/` avec `Authorization: Bearer <access_token>`

8. **Profil voyageur** :
   - GET `/api/users/<user_id>/travel-profile/` avec `Authorization: Bearer <access_token>`

## Technologies utilisées

- Python 3.x
- Django 5.x
- Django REST Framework
- Django REST Framework SimpleJWT (JWT)
- Scikit-learn (KNN, KMeans)
- PostgreSQL / SQLite (selon configuration)

## Remarques

- Les recommandations sont générées à partir des préférences utilisateur et des données des destinations.
- Si KNN ne renvoie aucune recommandation, l’application retourne les destinations les plus populaires.
- L’historique des recommandations est conservé pour chaque utilisateur.

