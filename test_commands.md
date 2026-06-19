# Commandes de Test pour le Système d'Inscription

Voici les commandes `curl` pour tester votre API. Assurez-vous que votre serveur est lancé avec `uvicorn main:app --reload`.

> [!NOTE]
> Remplacez les UUID par des valeurs réelles générées lors de vos tests.

### 1. Créer une Filière, Catégorie et Lieu
```bash
curl -X POST http://127.0.0.1:8000/filieres/ -H "Content-Type: application/json" -d '{"nom_filiere": "Informatique"}'
curl -X POST http://127.0.0.1:8000/categories/ -H "Content-Type: application/json" -d '{"libelle": "Conférence"}'
curl -X POST http://127.0.0.1:8000/lieux/ -H "Content-Type: application/json" -d '{"nom_lieu": "Amphi A", "ville": "Paris"}'
```

### 2. Créer un Utilisateur (Organisateur)
```bash
# Remplacez l'ID par un UUID valide (ex: généré par Supabase ou un site comme uuidgenerator.net)
ORG_ID="550e8400-e29b-41d4-a716-446655440000"
curl -X POST http://127.0.0.1:8000/utilisateurs/ -H "Content-Type: application/json" -d "{
  \"id_utilisateur\": \"$ORG_ID\",
  \"nom\": \"Jean Organisateur\",
  \"email\": \"jean@univ.fr\",
  \"role\": \"Organisateur\"
}"
```

### 3. Créer un Événement (avec capacité limitée à 1 pour le test)
```bash
# Remplacez les IDs par ceux obtenus à l'étape 1
CAT_ID="votre-id-categorie"
LIEU_ID="votre-id-lieu"

curl -X POST http://127.0.0.1:8000/utilisateurs/$ORG_ID/evenements/ -H "Content-Type: application/json" -d "{
  \"titre\": \"Atelier FastAPI\",
  \"description\": \"Apprendre FastAPI en 1h\",
  \"date_evenement\": \"2024-12-25T10:00:00\",
  \"capacite_max\": 1,
  \"id_categorie\": \"$CAT_ID\",
  \"id_lieu\": \"$LIEU_ID\"
}"
```

### 4. Tester l'Inscription
```bash
EVENT_ID="votre-id-evenement"
USER_ID="un-autre-uuid-utilisateur"

# Créer l'étudiant d'abord
curl -X POST http://127.0.0.1:8000/utilisateurs/ -H "Content-Type: application/json" -d "{
  \"id_utilisateur\": \"$USER_ID\",
  \"nom\": \"Alice Etudiante\",
  \"email\": \"alice@univ.fr\",
  \"role\": \"Etudiant\"
}"

# S'inscrire (Réussite attendue)
curl -X POST http://127.0.0.1:8000/evenements/$EVENT_ID/inscrire/$USER_ID

# Retenter l'inscription (Erreur attendue : Déjà inscrit)
curl -X POST http://127.0.0.1:8000/evenements/$EVENT_ID/inscrire/$USER_ID

# Tenter d'inscrire un 2ème utilisateur (Erreur attendue : Événement complet)
USER2_ID="uuid-2"
curl -X POST http://127.0.0.1:8000/utilisateurs/ -H "Content-Type: application/json" -d "{\"id_utilisateur\": \"$USER2_ID\", \"nom\": \"Bob\", \"email\": \"bob@univ.fr\"}"
curl -X POST http://127.0.0.1:8000/evenements/$EVENT_ID/inscrire/$USER2_ID
```
