# Gestion d'Événements Universitaires - API FastAPI

Cette API permet de gérer les événements au sein d'une université. Elle inclut la gestion des utilisateurs (étudiants, organisateurs, administrateurs), des filières, des catégories d'événements et des inscriptions.

Le projet est conçu pour fonctionner avec **PostgreSQL** et est prêt pour une intégration avec **Supabase**.

## Fonctionnalités

-   **Gestion des Utilisateurs** : Création de profils liés à l'authentification Supabase.
-   **Gestion des Événements** : Création, consultation et organisation d'événements universitaires.
-   **Système d'Inscription** : Inscription des étudiants aux événements.
-   **Données de Référence** : Gestion des filières, lieux et catégories thématiques.
-   **Architecture Propre** : Séparation des modèles, schémas (Pydantic), et logique CRUD.

## Technologies utilisées

-   **FastAPI** : Framework web moderne et rapide.
-   **SQLAlchemy** : ORM pour l'interaction avec la base de données.
-   **PostgreSQL** : Base de données relationnelle.
-   **Pydantic** : Validation des données et schémas.
-   **Python-dotenv** : Gestion des variables d'environnement.

##  Installation et Lancement

### 1. Cloner le projet
```bash
git clone <url-du-repo>
cd fastapi
```

### 2. Créer un environnement virtuel
```bash
python -m venv venv
source venv/bin/activate  # Sur Windows: venv\Scripts\activate
```

### 3. Installer les dépendances
```bash
pip install -r requirements.txt
```

### 4. Configurer les variables d'environnement
Créez un fichier `.env` à la racine du projet et ajoutez votre URL PostgreSQL :
```env
DATABASE_URL=postgresql://user:password@localhost:5432/nom_db
```

### 5. Lancer l'API
```bash
uvicorn main:app --reload
```

L'API sera disponible sur `http://127.0.0.1:8000`.
Accédez à la documentation interactive (Swagger) sur `http://127.0.0.1:8000/docs`.

##  Structure du Projet

-   `main.py` : Point d'entrée de l'application et définition des routes.
-   `models.py` : Modèles SQLAlchemy (schéma de la base de données).
-   `schemas.py` : Modèles Pydantic pour la validation des données.
-   `crud.py` : Fonctions d'interaction avec la base de données.
-   `database.py` : Configuration de la connexion SQLAlchemy.
-   `.gitignore` : Fichiers et dossiers exclus de Git (dont le `.env`).
