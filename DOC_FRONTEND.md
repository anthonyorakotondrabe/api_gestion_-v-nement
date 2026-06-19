& # 📚 Documentation API - Gestion Événements Universitaires

Cette documentation est destinée aux développeurs Front-End pour l'intégration du système d'authentification et de gestion des événements.

## 🔑 Authentification (JWT)

L'API utilise des **JSON Web Tokens (JWT)**. Le token doit être envoyé dans l'en-tête de chaque requête protégée.

**En-tête requis :**
`Authorization: Bearer <votre_access_token>`

---

### 1. Inscription (Register)
Crée un nouveau compte utilisateur.

- **URL** : `/auth/register`
- **Méthode** : `POST`
- **Corps de la requête (JSON)** :
```json
{
  "nom": "Jean Dupont",
  "email": "jean.dupont@univ.fr",
  "password": "un_mot_de_passe_robuste",
  "role": "Etudiant",
  "id_filiere": "uuid-de-la-filiere (optionnel)"
}
```
- **Réponse de succès (200 OK)** : Retourne l'objet utilisateur créé (sans le mot de passe).

---

### 2. Connexion (Login)
Authentifie l'utilisateur et retourne un token.

- **URL** : `/auth/login`
- **Méthode** : `POST`
- **Corps de la requête** : `application/x-www-form-urlencoded`
    - `username` : l'email de l'utilisateur
    - `password` : le mot de passe
- **Réponse de succès (200 OK)** :
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```
> [!IMPORTANT]
> Le token doit être stocké côté client (localStorage, sessionStorage ou Cookie sécurisé) pour les requêtes ultérieures.

---

### 3. Profil Utilisateur (Me)
Récupère les informations de l'utilisateur actuellement connecté.

- **URL** : `/utilisateurs/me`
- **Méthode** : `GET`
- **Protection** : Requis un Token valide.
- **Réponse de succès (200 OK)** :
```json
{
  "id_utilisateur": "uuid-de-l-utilisateur",
  "nom": "Jean Dupont",
  "email": "jean.dupont@univ.fr",
  "role": "Etudiant",
  "id_filiere": "uuid-filiere"
}
```

---

### 4. Déconnexion (Logout)
Comme l'API est **stateless** (sans état), la déconnexion se gère exclusivement côté Front-End.
- **Action** : Supprimer le `access_token` du stockage local du navigateur.
- **Redirection** : Rediriger l'utilisateur vers la page de connexion.

---

## 📅 Événements

### Lister les événements (Public)
- **URL** : `/evenements/`
- **Méthode** : `GET`

### S'inscrire à un événement (Protégé)
- **URL** : `/evenements/{id_evenement}/inscrire`
- **Méthode** : `POST`
- **Protection** : Requis un Token valide. L'utilisateur est identifié via le token, aucun corps de requête n'est nécessaire.

### Voir mes inscriptions (Étudiant)
- **URL** : `/utilisateurs/me/inscriptions`
- **Méthode** : `GET`
- **Protection** : Requis un Token valide.

### Voir les inscrits d'un événement (Organisateur/Admin)
- **URL** : `/evenements/{id_evenement}/inscriptions`
- **Méthode** : `GET`
- **Protection** : Requis un Token Admin ou du Créateur de l'événement.

### Annuler une inscription (Utilisateur/Organisateur/Admin)
- **URL** : `/inscriptions/{id_inscription}`
- **Méthode** : `DELETE`
- **Protection** : L'utilisateur pour sa propre inscription, l'organisateur pour son événement, ou un Admin.

---

## ⚙️ Administration (Admin Uniquement)

Ces endpoints sont réservés aux utilisateurs ayant le rôle `Admin`.

### Filières
- `GET /filieres/` : Lister les filières.
- `POST /filieres/` : Créer une filière.
- `PUT /filieres/{id}` : Modifier une filière.
- `DELETE /filieres/{id}` : Supprimer une filière.

### Catégories
- `GET /categories/` : Lister les catégories.
- `POST /categories/` : Créer une catégorie.
- `PUT /categories/{id}` : Modifier une catégorie.
- `DELETE /categories/{id}` : Supprimer une catégorie.

### Lieux
- `GET /lieux/` : Lister les lieux.
- `POST /lieux/` : Créer un lieu.
- `PUT /lieux/{id}` : Modifier un lieu.
- `DELETE /lieux/{id}` : Supprimer un lieu.

---

### Créer un événement (Organisateur/Admin)
- **URL** : `/evenements/`
- **Méthode** : `POST`
- **Protection** : Requis un Token avec rôle `Organisateur` ou `Admin`.
- **Corps (JSON)** : Voir `EvenementCreate` dans Swagger.

### Modifier un événement (Organisateur/Admin)
- **URL** : `/evenements/{id_evenement}`
- **Méthode** : `PUT`
- **Protection** : Requis un Token Admin ou du Créateur de l'événement.
- **Corps (JSON)** : Champs optionnels à mettre à jour.

### Supprimer un événement (Organisateur/Admin)
- **URL** : `/evenements/{id_evenement}`
- **Méthode** : `DELETE`
- **Protection** : Requis un Token Admin ou du Créateur de l'événement.

---

## ⚠️ Gestion des Erreurs

| Code HTTP | Description | Solution suggérée |
| :--- | :--- | :--- |
| **400** | Bad Request | Vérifier les données envoyées (ex: email déjà utilisé, événement complet). |
| **401** | Unauthorized | Token manquant ou expiré. Rediriger vers `/login`. |
| **403** | Forbidden | L'utilisateur n'a pas les droits (ex: un étudiant qui tente de créer un lieu). |
| **404** | Not Found | La ressource n'existe pas. |
| **422** | Unprocessable Entity | Format de données incorrect (ex: email invalide). |

---

## 💡 Conseils d'Intégration
- **Swagger UI** : L'API propose une documentation interactive complète sur `http://127.0.0.1:8000/docs`. Vous pouvez y tester chaque endpoint en direct.
- **Intercepteur** : Utilisez un intercepteur (ex: avec `Axios`) pour ajouter automatiquement l'en-tête `Authorization` si le token est présent dans le stockage local.
