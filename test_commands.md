# Commandes de Test pour l'API Gestion d'Événements

Voici les commandes `curl` pour tester votre API, y compris les restrictions de rôle (RBAC) et la gestion des données de référence.

### 1. Préparation et Administration (Admin)

#### Création et Gestion des Filières
```bash
# Inscription Admin
curl -X POST http://127.0.0.1:8000/auth/register -H "Content-Type: application/json" -d '{
  "nom": "Admin", "email": "admin@univ.fr", "password": "admin_password", "role": "Admin"
}'

# Connexion Admin (récupérez le token)
curl -X POST http://127.0.0.1:8000/auth/login -d "username=admin@univ.fr&password=admin_password"

# Créer une filière
curl -X POST http://127.0.0.1:8000/filieres/ -H "Authorization: Bearer $TOKEN_ADMIN" -H "Content-Type: application/json" -d '{"nom_filiere": "Informatique"}'

# Modifier une filière
curl -X PUT http://127.0.0.1:8000/filieres/$ID_FILIERE -H "Authorization: Bearer $TOKEN_ADMIN" -H "Content-Type: application/json" -d '{"nom_filiere": "Informatique Avancée"}'
```

#### Création et Gestion des Catégories et Lieux
```bash
# Créer une catégorie
curl -X POST http://127.0.0.1:8000/categories/ -H "Authorization: Bearer $TOKEN_ADMIN" -H "Content-Type: application/json" -d '{"libelle": "Conférence"}'

# Créer un lieu
curl -X POST http://127.0.0.1:8000/lieux/ -H "Authorization: Bearer $TOKEN_ADMIN" -H "Content-Type: application/json" -d '{"nom_lieu": "Amphi A", "ville": "Paris"}'
```

#### Gestion des Utilisateurs (Admin)
```bash
# Lister les utilisateurs
curl -X GET http://127.0.0.1:8000/utilisateurs/ -H "Authorization: Bearer $TOKEN_ADMIN"

# Modifier le rôle d'un utilisateur (ex: promouvoir en Organisateur)
curl -X PUT http://127.0.0.1:8000/utilisateurs/$ID_UTILISATEUR \
  -H "Authorization: Bearer $TOKEN_ADMIN" \
  -H "Content-Type: application/json" \
  -d '{"role": "Organisateur"}'

# Supprimer un utilisateur
curl -X DELETE http://127.0.0.1:8000/utilisateurs/$ID_UTILISATEUR -H "Authorization: Bearer $TOKEN_ADMIN"
```

### 2. Gestion des Événements (CRUD & RBAC)

#### Création (Organisateur)
```bash
# S'inscrire en tant qu'Organisateur
curl -X POST http://127.0.0.1:8000/auth/register -H "Content-Type: application/json" -d '{
  "nom": "Organisateur", "email": "org@univ.fr", "password": "org_password", "role": "Organisateur"
}'

# Se connecter pour avoir le TOKEN_ORG
curl -X POST http://127.0.0.1:8000/auth/login -d "username=org@univ.fr&password=org_password"

# Créer un événement
curl -X POST http://127.0.0.1:8000/evenements/ \
  -H "Authorization: Bearer $TOKEN_ORG" \
  -H "Content-Type: application/json" \
  -d '{
    "titre": "Conférence IA",
    "description": "Tout sur le futur",
    "date_evenement": "2024-12-01T14:00:00",
    "capacite_max": 50,
    "id_categorie": "uuid-cat",
    "id_lieu": "uuid-lieu"
  }'
```

#### Tentative de modification par un Étudiant (Échec attendu)
```bash
# S'inscrire en tant qu'Étudiant
curl -X POST http://127.0.0.1:8000/auth/register -H "Content-Type: application/json" -d '{
  "nom": "Etudiant", "email": "etud@univ.fr", "password": "etud_password", "role": "Etudiant"
}'

# Se connecter pour avoir le TOKEN_ETUD
curl -X POST http://127.0.0.1:8000/auth/login -d "username=etud@univ.fr&password=etud_password"

# Tenter de modifier un événement (Erreur 403)
curl -X PUT http://127.0.0.1:8000/evenements/$EVENT_ID \
  -H "Authorization: Bearer $TOKEN_ETUD" \
  -d '{"titre": "Titre Piraté"}'
```

#### Modification par l'Organisateur (Réussite)
```bash
curl -X PUT http://127.0.0.1:8000/evenements/$EVENT_ID \
  -H "Authorization: Bearer $TOKEN_ORG" \
  -H "Content-Type: application/json" \
  -d '{"titre": "Nouveau Titre Officiel"}'
```

#### Suppression par l'Admin (Réussite)
```bash
curl -X DELETE http://127.0.0.1:8000/evenements/$EVENT_ID \
  -H "Authorization: Bearer $TOKEN_ADMIN"
```
