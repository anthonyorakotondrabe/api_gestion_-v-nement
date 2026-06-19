# 📌 Résumé de l'API - Gestion Événements Universitaires

Ce document offre une vue d'ensemble rapide de l'API FastAPI et de son fonctionnement.

## 🏗️ Architecture & Technologies
- **Framework** : FastAPI (Python)
- **Base de données** : PostgreSQL (Compatible Supabase)
- **ORM** : SQLAlchemy (Modèles dans `models.py`)
- **Validation** : Pydantic V2 (Schémas dans `schemas.py`)
- **Sécurité** : JWT (JSON Web Tokens) avec hachage Bcrypt + SHA-256.

---

## 🔐 Flux d'Authentification
1. **Inscription** : `POST /auth/register` (Crée l'utilisateur).
2. **Connexion** : `POST /auth/login` (Retourne un `access_token`).
3. **Usage** : Envoyer le token dans le header `Authorization: Bearer <token>` pour les routes protégées.

---

## 📋 Liste des Endpoints Principaux

### 🔑 Authentification
- `POST /auth/register` : Création de compte.
- `POST /auth/login` : Connexion (format form-data).

### 👥 Utilisateurs
- `GET /utilisateurs/me` : Profil de l'utilisateur connecté.
- `GET /utilisateurs/me/inscriptions` : Liste des événements de l'étudiant.
- `GET /utilisateurs/` : Liste tous les utilisateurs (**Admin**).
- `GET /utilisateurs/{id}` : Détails d'un utilisateur (**Admin**).
- `PUT /utilisateurs/{id}` : Modifier un utilisateur (**Admin**).
- `DELETE /utilisateurs/{id}` : Supprimer un utilisateur (**Admin**).

### 📅 Événements
- `GET /evenements/` : Liste tous les événements (Public).
- `POST /evenements/` : Créer un événement (**Organisateur/Admin**).
- `PUT /evenements/{id}` : Modifier un événement (**Créateur/Admin**).
- `DELETE /evenements/{id}` : Supprimer un événement (**Créateur/Admin**).

### 📝 Inscriptions
- `POST /evenements/{id}/inscrire` : S'inscrire à un événement (Vérifie la capacité).
- `DELETE /inscriptions/{id}` : Annuler une inscription.

### ⚙️ Administration (Admin uniquement)
<<<<<<< HEAD
- `POST /filieres/` : Créer une filière.
- `POST /categories/` : Créer une catégorie.
- `POST /lieux/` : Créer un lieu.

---

## 🚦 Codes de Statut Communs
- **200 OK** : Succès.
- **201 Created** : Ressource créée.
- **204 No Content** : Suppression réussie.
- **400 Bad Request** : Erreur métier (ex: événement complet, doublon).
- **401 Unauthorized** : Token invalide ou manquant.
- **403 Forbidden** : Rôle insuffisant ou n'est pas le propriétaire.
- **404 Not Found** : Ressource inexistante.
=======
- `GET /filieres/` : Lister les filières.
- `POST /filieres/` : Créer une filière.
- `PUT /filieres/{id}` : Modifier une filière.
- `DELETE /filieres/{id}` : Supprimer une filière.

- `GET /categories/` : Lister les catégories.
- `POST /categories/` : Créer une catégorie.
- `PUT /categories/{id}` : Modifier une catégorie.
- `DELETE /categories/{id}` : Supprimer une catégorie.

- `GET /lieux/` : Lister les lieux.
- `POST /lieux/` : Créer un lieu.
- `PUT /lieux/{id}` : Modifier un lieu.
- `DELETE /lieux/{id}` : Supprimer un lieu.
>>>>>>> admin

---

## 🛠️ Documentation Interactive
L'API génère automatiquement deux interfaces de test :
- **Swagger UI** : `http://127.0.0.1:8000/docs` (Recommandé)
- **ReDoc** : `http://127.0.0.1:8000/redoc`
