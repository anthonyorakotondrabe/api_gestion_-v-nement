from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID
from datetime import timedelta

import models, schemas, crud, auth
from database import engine, get_db

"""
Point d'entrée principal de l'API FastAPI.
Ce fichier initialise l'application, crée les tables et définit les routes.
"""

# Création automatique des tables dans la base de données au démarrage (utile en local)
models.Base.metadata.create_all(bind=engine)

# Initialisation de l'application FastAPI
app = FastAPI(
    title="Gestion Événements Universitaires",
    description="API pour la gestion des événements universitaires avec Authentification JWT."
)

@app.get("/")
def read_root():
    """Route d'accueil de l'API."""
    return {"message": "Bienvenue sur l'API de gestion d'événements universitaires"}

# --- Authentification ---

@app.post("/auth/register", response_model=schemas.Utilisateur, tags=["Authentification"])
def register(utilisateur: schemas.UtilisateurCreate, db: Session = Depends(get_db)):
    """Crée un compte utilisateur avec mot de passe haché."""
    db_user = crud.get_utilisateur_by_email(db, email=utilisateur.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Cet email est déjà utilisé.")
    return crud.create_utilisateur(db=db, utilisateur=utilisateur)

@app.post("/auth/login", response_model=schemas.Token, tags=["Authentification"])
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """Connecte un utilisateur et retourne un token JWT (Utilisez l'email dans le champ username)."""
    user = crud.get_utilisateur_by_email(db, email=form_data.username)
    if not user or not auth.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou mot de passe incorrect",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = auth.create_access_token(data={"sub": str(user.id_utilisateur)})
    return {"access_token": access_token, "token_type": "bearer"}

# --- Routes Utilisateurs ---

@app.get("/utilisateurs/me", response_model=schemas.Utilisateur, tags=["Utilisateurs"])
def read_users_me(current_user: models.Utilisateur = Depends(auth.get_current_user)):
    """Récupère les informations de l'utilisateur connecté."""
    return current_user

# --- Routes Événements ---

@app.get("/evenements/", response_model=List[schemas.Evenement], tags=["Événements"])
def read_evenements(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Récupère la liste de tous les événements (Public)."""
    return crud.get_evenements(db, skip=skip, limit=limit)

@app.post("/evenements/", response_model=schemas.Evenement, tags=["Événements"])
def create_evenement(
    evenement: schemas.EvenementCreate,
    db: Session = Depends(get_db),
    current_user: models.Utilisateur = Depends(auth.get_current_user)
):
    """Crée un événement (Réservé aux utilisateurs connectés)."""
    # Vérification du rôle si besoin
    if current_user.role not in [models.RoleUtilisateur.Organisateur, models.RoleUtilisateur.Admin]:
        raise HTTPException(status_code=403, detail="Seuls les organisateurs peuvent créer des événements.")
    return crud.create_evenement(db=db, evenement=evenement, createur_id=current_user.id_utilisateur)

@app.put("/evenements/{id_evenement}", response_model=schemas.Evenement, tags=["Événements"])
def update_evenement(
    id_evenement: UUID,
    evenement_update: schemas.EvenementUpdate,
    db: Session = Depends(get_db),
    current_user: models.Utilisateur = Depends(auth.get_current_user)
):
    """Met à jour un événement (Réservé Organisateur/Admin)."""
    db_evenement = crud.get_evenement(db, id_evenement=id_evenement)
    if not db_evenement:
        raise HTTPException(status_code=404, detail="Événement non trouvé.")

    # Vérification des droits : Admin ou Créateur de l'événement
    if current_user.role != models.RoleUtilisateur.Admin and db_evenement.createur_id != current_user.id_utilisateur:
        raise HTTPException(status_code=403, detail="Vous n'avez pas le droit de modifier cet événement.")

    return crud.update_evenement(db=db, db_evenement=db_evenement, evenement_update=evenement_update)

@app.delete("/evenements/{id_evenement}", status_code=status.HTTP_204_NO_CONTENT, tags=["Événements"])
def delete_evenement(
    id_evenement: UUID,
    db: Session = Depends(get_db),
    current_user: models.Utilisateur = Depends(auth.get_current_user)
):
    """Supprime un événement (Réservé Organisateur/Admin)."""
    db_evenement = crud.get_evenement(db, id_evenement=id_evenement)
    if not db_evenement:
        raise HTTPException(status_code=404, detail="Événement non trouvé.")

    # Vérification des droits : Admin ou Créateur de l'événement
    if current_user.role != models.RoleUtilisateur.Admin and db_evenement.createur_id != current_user.id_utilisateur:
        raise HTTPException(status_code=403, detail="Vous n'avez pas le droit de supprimer cet événement.")

    crud.delete_evenement(db=db, db_evenement=db_evenement)
    return None

# --- Routes Inscriptions ---

@app.post("/evenements/{id_evenement}/inscrire", response_model=schemas.Inscription, tags=["Inscriptions"])
def register_for_event(
    id_evenement: UUID,
    db: Session = Depends(get_db),
    current_user: models.Utilisateur = Depends(auth.get_current_user)
):
    """
    Inscrit l'utilisateur connecté à un événement (Requiert d'être connecté).
    """
    id_utilisateur = current_user.id_utilisateur

    # 1. Vérifier si l'événement existe
    db_event = crud.get_evenement(db, id_evenement=id_evenement)
    if not db_event:
        raise HTTPException(status_code=404, detail="Événement non trouvé.")

    # 2. Vérifier si l'utilisateur est déjà inscrit
    db_inscription = crud.get_inscription(db, id_evenement=id_evenement, id_utilisateur=id_utilisateur)
    if db_inscription:
        raise HTTPException(status_code=400, detail="Vous êtes déjà inscrit à cet événement.")

    # 3. Vérifier la capacité maximale
    count = crud.count_inscriptions_evenement(db, id_evenement=id_evenement)
    if count >= db_event.capacite_max:
        raise HTTPException(status_code=400, detail="L'événement est complet.")

    # 4. Créer l'inscription
    return crud.create_inscription(db=db, id_evenement=id_evenement, id_utilisateur=id_utilisateur)

# --- Routes de Référence (Administration) ---

@app.post("/filieres/", response_model=schemas.Filiere, tags=["Administration"])
def create_filiere(
    filiere: schemas.FiliereCreate,
    db: Session = Depends(get_db),
    current_user: models.Utilisateur = Depends(auth.get_current_user)
):
    """Crée une nouvelle filière (Réservé Admin)."""
    if current_user.role != models.RoleUtilisateur.Admin:
        raise HTTPException(status_code=403, detail="Réservé aux administrateurs.")
    return crud.create_filiere(db=db, filiere=filiere)

@app.post("/categories/", response_model=schemas.Categorie, tags=["Administration"])
def create_categorie(
    categorie: schemas.CategorieCreate,
    db: Session = Depends(get_db),
    current_user: models.Utilisateur = Depends(auth.get_current_user)
):
    """Crée une nouvelle catégorie (Réservé Admin)."""
    if current_user.role != models.RoleUtilisateur.Admin:
        raise HTTPException(status_code=403, detail="Réservé aux administrateurs.")
    return crud.create_categorie(db=db, categorie=categorie)

@app.post("/lieux/", response_model=schemas.Lieu, tags=["Administration"])
def create_lieu(
    lieu: schemas.LieuCreate,
    db: Session = Depends(get_db),
    current_user: models.Utilisateur = Depends(auth.get_current_user)
):
    """Crée un nouveau lieu (Réservé Admin)."""
    if current_user.role != models.RoleUtilisateur.Admin:
        raise HTTPException(status_code=403, detail="Réservé aux administrateurs.")
    return crud.create_lieu(db=db, lieu=lieu)
