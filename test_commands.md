# Commandes de Test pour l'API Gestion d'Événements

Voici les commandes `curl` pour tester votre API, y compris les restrictions de rôle (RBAC).

### 1. Préparation (Admin)
Connectez-vous avec un compte **Admin** pour créer les données de base (Filière, Catégorie, Lieu).
```bash
# S'inscrire en tant qu'Admin
curl -X POST http://127.0.0.1:8000/auth/register -H "Content-Type: application/json" -d '{
  "nom": "Admin", "email": "admin@univ.fr", "password": "admin_password", "role": "Admin"
}'

# Se connecter pour avoir le TOKEN_ADMIN
curl -X POST http://127.0.0.1:8000/auth/login -d "username=admin@univ.fr&password=admin_password"
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
