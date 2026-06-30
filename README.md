# Gestion d'Événements Universitaires - API FastAPI

Cette API permet de gérer les événements au sein d'une université. Elle inclut la gestion des utilisateurs (étudiants, organisateurs, administrateurs), des filières, des catégories d'événements et des inscriptions.

Le projet est conçu avec une architecture en couches pour assurer la maintenabilité et la séparation des responsabilités.

## 🏗 Architecture du Projet

L'API suit un pattern classique d'architecture en couches pour les applications FastAPI :

### 1. Couche de Données (Models)
- **`database.py`** : Configuration de SQLAlchemy. Gère la connexion à PostgreSQL, la création de l'engine et la session de base de données.
- **`models.py`** : Définition des entités de la base de données via l'ORM SQLAlchemy. Chaque classe représente une table (Utilisateur, Evenement, Inscription, etc.) avec ses relations.

### 2. Couche de Validation (Schemas)
- **`schemas.py`** : Utilise Pydantic pour définir les schémas de données. Ces modèles assurent la validation des données entrantes (Input) et le formatage des données sortantes (Output). Cela permet de séparer la structure de la base de données de ce qui est réellement exposé via l'API.

### 3. Couche d'Accès aux Données (CRUD)
- **`crud.py`** : Regroupe toute la logique d'interaction avec la base de données. Cette couche fait le pont entre les schémas Pydantic et les modèles SQLAlchemy, permettant de garder les routes (endpoints) propres et focalisées sur la gestion des requêtes HTTP.

### 4. Couche de Sécurité & Authentification
- **`auth.py`** : Gère la sécurité de l'application. Elle contient la logique de hachage des mots de passe (bcrypt), la génération et la validation des tokens JWT (JSON Web Tokens), ainsi que les dépendances pour récupérer l'utilisateur courant.

### 5. Couche de Transport / Points d'Entrée
- **`main.py`** : Cœur de l'application. Il initialise FastAPI, configure les middlewares (CORS), et définit tous les points d'entrée (endpoints) de l'API. Il utilise l'injection de dépendances pour intégrer la session de base de données et l'authentification.

---

## 🛠 Technologies utilisées

-   **FastAPI** : Framework web moderne et rapide.
-   **SQLAlchemy** : ORM pour l'interaction avec la base de données.
-   **PostgreSQL** : Base de données relationnelle.
-   **Pydantic** : Validation des données et schémas.
-   **Python-dotenv** : Gestion des variables d'environnement.
-   **Passlib (bcrypt)** : Hachage sécurisé des mots de passe.
-   **PyJWT** : Gestion des tokens JWT.

---

## 🚀 Installation et Lancement

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
Créez un fichier `.env` à la racine du projet :
```env
DATABASE_URL=postgresql://user:password@localhost:5432/nom_db
SECRET_KEY=votre_cle_secrete_tres_longue_et_aleatoire
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### 5. Lancer l'API
```bash
uvicorn main:app --reload
```

L'API sera disponible sur `http://127.0.0.1:8000`.
Accédez à la documentation interactive (Swagger) sur `http://127.0.0.1:8000/docs`.
