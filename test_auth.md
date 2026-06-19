# Tests du Système d'Authentification

Suivez ces étapes pour tester l'inscription, la connexion et l'accès aux routes protégées.

### 1. Inscription (Register)
Créez un nouvel utilisateur avec un mot de passe (L'ID est optionnel).
```bash
curl -X POST http://127.0.0.1:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "nom": "Alice Test",
    "email": "alice@test.fr",
    "password": "mon_mot_de_passe_secret",
    "role": "Etudiant"
  }'
```

### 2. Connexion (Login)
Récupérez votre token JWT.
```bash
curl -X POST http://127.0.0.1:8000/auth/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=alice@test.fr&password=mon_mot_de_passe_secret"
```
**Copiez la valeur de `access_token` retournée.**

### 3. Accès à une route protégée
Utilisez le token pour voir votre profil.
```bash
TOKEN="votre_access_token_ici"

curl -X GET http://127.0.0.1:8000/utilisateurs/me \
  -H "Authorization: Bearer $TOKEN"
```

### 4. Inscription à un événement (Protégée)
Seul un utilisateur connecté peut s'inscrire.
```bash
EVENT_ID="votre_id_evenement"

curl -X POST http://127.0.0.1:8000/evenements/$EVENT_ID/inscrire \
  -H "Authorization: Bearer $TOKEN"
```

### 5. Déconnexion
Comme nous utilisons des JWT, la déconnexion se fait côté client en supprimant simplement le token de la mémoire ou du stockage local. L'API est sans état (stateless).
