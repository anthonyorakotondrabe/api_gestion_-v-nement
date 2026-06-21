from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
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
    title="Gestion Événements Universitaires ",
description="API pour la gestion des événements universitaires par Anthonyo RAKOTONDRABE"
)

# Configuration du Middleware CORS
origins = [
    "http://localhost:5173",
    "https://unievent-eta.vercel.app",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    """Route d'accueil de l'API."""
    return {"message": "Bienvenue sur l'API de gestion d'événements universitaires conçu par Anthonyo RAKOTONDRABE"}

# --- Authentification ---

@app.post("/auth/register", response_model=schemas.Utilisateur, tags=["Authentification"])
def register(utilisateur: schemas.UtilisateurCreate, db: Session = Depends(get_db)):
    """
    Crée un compte utilisateur.
    Sécurité :Forcé ho Etudiant foana ny rôle eto pour raison de sécrité.
    """
    # Forcer le rôle par défaut pour toute inscription publique
    utilisateur.role = models.RoleUtilisateur.Etudiant

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

@app.get("/utilisateurs/", response_model=List[schemas.Utilisateur], tags=["Utilisateurs"])
def read_utilisateurs(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: models.Utilisateur = Depends(auth.get_current_user)
):
    """Lister tous les utilisateurs (Réservé Admin)."""
    if current_user.role != models.RoleUtilisateur.Admin:
        raise HTTPException(status_code=403, detail="Réservé aux administrateurs.")
    return crud.get_utilisateurs(db, skip=skip, limit=limit)

@app.get("/utilisateurs/{id_utilisateur}", response_model=schemas.Utilisateur, tags=["Utilisateurs"])
def read_utilisateur(
    id_utilisateur: UUID,
    db: Session = Depends(get_db),
    current_user: models.Utilisateur = Depends(auth.get_current_user)
):
    """Récupérer un utilisateur spécifique (Réservé Admin/Organisateur)."""
    if current_user.role not in [models.RoleUtilisateur.Admin, models.RoleUtilisateur.Organisateur]:
        raise HTTPException(status_code=403, detail="Réservé aux administrateurs ou organisateurs.")
    db_user = crud.get_utilisateur(db, id_utilisateur=id_utilisateur)
    if not db_user:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé.")
    return db_user

@app.put("/utilisateurs/{id_utilisateur}", response_model=schemas.Utilisateur, tags=["Utilisateurs"])
def update_utilisateur(
    id_utilisateur: UUID,
    user_update: schemas.UtilisateurUpdate,
    db: Session = Depends(get_db),
    current_user: models.Utilisateur = Depends(auth.get_current_user)
):
    """Mettre à jour un utilisateur (Réservé Admin)."""
    if current_user.role != models.RoleUtilisateur.Admin:
        raise HTTPException(status_code=403, detail="Réservé aux administrateurs.")

    db_user = crud.get_utilisateur(db, id_utilisateur=id_utilisateur)
    if not db_user:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé.")

    return crud.update_utilisateur(db=db, db_user=db_user, user_update=user_update)

@app.delete("/utilisateurs/{id_utilisateur}", status_code=status.HTTP_204_NO_CONTENT, tags=["Utilisateurs"])
def delete_utilisateur(
    id_utilisateur: UUID,
    db: Session = Depends(get_db),
    current_user: models.Utilisateur = Depends(auth.get_current_user)
):
    """Supprimer un utilisateur (Réservé Admin)."""
    if current_user.role != models.RoleUtilisateur.Admin:
        raise HTTPException(status_code=403, detail="Réservé aux administrateurs.")

    db_user = crud.get_utilisateur(db, id_utilisateur=id_utilisateur)
    if not db_user:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé.")

    crud.delete_utilisateur(db=db, db_user=db_user)
    return None

# --- Routes Événements ---

@app.get("/evenements/", response_model=List[schemas.Evenement], tags=["Événements"])
def read_evenements(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Récupère la liste de tous les événements (Public)."""
    return crud.get_evenements(db, skip=skip, limit=limit)

@app.get("/evenements/{id_evenement}", response_model=schemas.Evenement, tags=["Événements"])
def read_evenement(id_evenement: UUID, db: Session = Depends(get_db)):
    """Récupère un événement spécifique par son ID (Public)."""
    db_evenement = crud.get_evenement(db, id_evenement=id_evenement)
    if not db_evenement:
        raise HTTPException(status_code=404, detail="Événement non trouvé.")
    return db_evenement

@app.post("/evenements/", response_model=schemas.Evenement, tags=["Événements"])
def create_evenement(
    evenement: schemas.EvenementCreate,
    db: Session = Depends(get_db),
    current_user: models.Utilisateur = Depends(auth.get_current_user)
):
    """Crée un événement (Réservé Organisateur/Admin)."""
    # Vérification du rôle
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

    # Vérification des droits : Admin ou (Organisateur ET Créateur de l'événement)
    if current_user.role != models.RoleUtilisateur.Admin:
        if current_user.role != models.RoleUtilisateur.Organisateur or db_evenement.createur_id != current_user.id_utilisateur:
            raise HTTPException(status_code=403, detail="Seul l'organisateur créateur de l'événement ou un administrateur peut modifier cet événement.")

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

    # Vérification des droits : Admin ou (Organisateur ET Créateur de l'événement)
    if current_user.role != models.RoleUtilisateur.Admin:
        if current_user.role != models.RoleUtilisateur.Organisateur or db_evenement.createur_id != current_user.id_utilisateur:
            raise HTTPException(status_code=403, detail="Vous n'avez pas les droits nécessaires pour supprimer cet événement.")

    crud.delete_evenement(db=db, db_evenement=db_evenement)
    return None

# --- Routes Inscriptions pour événement---

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

@app.get("/utilisateurs/me/inscriptions", response_model=List[schemas.Inscription], tags=["Inscriptions"])
def read_my_inscriptions(
    db: Session = Depends(get_db),
    current_user: models.Utilisateur = Depends(auth.get_current_user)
):
    """Récupère la liste des inscriptions de l'utilisateur connecté."""
    return crud.get_inscriptions_by_user(db, id_utilisateur=current_user.id_utilisateur)

@app.get("/evenements/{id_evenement}/inscriptions", response_model=List[schemas.Inscription], tags=["Inscriptions"])
def read_event_inscriptions(
    id_evenement: UUID,
    db: Session = Depends(get_db),
    current_user: models.Utilisateur = Depends(auth.get_current_user)
):
    """
    Récupère la liste des inscrits à un événement.
    Réservé à l'organisateur de l'événement ou à l'Admin.
    """
    db_event = crud.get_evenement(db, id_evenement=id_evenement)
    if not db_event:
        raise HTTPException(status_code=404, detail="Événement non trouvé.")

    # Vérification des droits : Admin ou (Organisateur ET Créateur de l'événement)
    if current_user.role != models.RoleUtilisateur.Admin:
        if current_user.role != models.RoleUtilisateur.Organisateur or db_event.createur_id != current_user.id_utilisateur:
            raise HTTPException(status_code=403, detail="Seul l'organisateur de l'événement ou un administrateur peut voir les inscriptions.")

    return crud.get_inscriptions_by_event(db, id_evenement=id_evenement)

@app.delete("/inscriptions/{id_inscription}", status_code=status.HTTP_204_NO_CONTENT, tags=["Inscriptions"])
def cancel_inscription(
    id_inscription: UUID,
    db: Session = Depends(get_db),
    current_user: models.Utilisateur = Depends(auth.get_current_user)
):
    """
    Annule une inscription.
    L'utilisateur peut annuler sa propre inscription.
    L'organisateur de l'événement ou l'Admin peuvent également annuler une inscription.
    """
    db_inscription = crud.get_inscription_by_id(db, id_inscription=id_inscription)
    if not db_inscription:
        raise HTTPException(status_code=404, detail="Inscription non trouvée.")

    db_event = crud.get_evenement(db, id_evenement=db_inscription.id_evenement)

    # Vérification des droits : Soit c'est l'étudiant lui-même, soit l'organisateur (créateur) de l'event, soit l'Admin
    is_owner = current_user.id_utilisateur == db_inscription.id_utilisateur
    is_admin = current_user.role == models.RoleUtilisateur.Admin
    is_organizer_of_event = (
        current_user.role == models.RoleUtilisateur.Organisateur and
        current_user.id_utilisateur == db_event.createur_id
    )

    if not (is_owner or is_admin or is_organizer_of_event):
        raise HTTPException(status_code=403, detail="Vous n'avez pas le droit d'annuler cette inscription.")

    crud.delete_inscription(db, db_inscription=db_inscription)
    return None

@app.put("/inscriptions/{id_inscription}", response_model=schemas.Inscription, tags=["Inscriptions"])
def update_inscription(
    id_inscription: UUID,
    inscription_update: schemas.InscriptionUpdate,
    db: Session = Depends(get_db),
    current_user: models.Utilisateur = Depends(auth.get_current_user)
):
    """
    Met à jour le statut d'une inscription.
    Réservé à l'organisateur de l'événement ou à l'Admin.
    """
    db_inscription = crud.get_inscription_by_id(db, id_inscription=id_inscription)
    if not db_inscription:
        raise HTTPException(status_code=404, detail="Inscription non trouvée.")

    db_event = crud.get_evenement(db, id_evenement=db_inscription.id_evenement)

    # Vérification des droits : Admin ou (Organisateur ET Créateur de l'événement)
    is_admin = current_user.role == models.RoleUtilisateur.Admin
    is_organizer_of_event = (
        current_user.role == models.RoleUtilisateur.Organisateur and
        current_user.id_utilisateur == db_event.createur_id
    )

    if not (is_admin or is_organizer_of_event):
        raise HTTPException(status_code=403, detail="Seul l'organisateur de l'événement ou un administrateur peut modifier cette inscription.")

    return crud.update_inscription(db=db, db_inscription=db_inscription, inscription_update=inscription_update)

# --- Routes de Référence (Administration) ---

@app.get("/filieres/", response_model=List[schemas.Filiere], tags=["Administration"])
def read_filieres(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Récupère la liste de toutes les filières."""
    return crud.get_filieres(db, skip=skip, limit=limit)

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

@app.put("/filieres/{id_filiere}", response_model=schemas.Filiere, tags=["Administration"])
def update_filiere(
    id_filiere: UUID,
    filiere_update: schemas.FiliereUpdate,
    db: Session = Depends(get_db),
    current_user: models.Utilisateur = Depends(auth.get_current_user)
):
    """Met à jour une filière (Réservé Admin)."""
    if current_user.role != models.RoleUtilisateur.Admin:
        raise HTTPException(status_code=403, detail="Réservé aux administrateurs.")
    db_filiere = crud.get_filiere(db, id_filiere=id_filiere)
    if not db_filiere:
        raise HTTPException(status_code=404, detail="Filière non trouvée.")
    return crud.update_filiere(db=db, db_filiere=db_filiere, filiere_update=filiere_update)

@app.delete("/filieres/{id_filiere}", status_code=status.HTTP_204_NO_CONTENT, tags=["Administration"])
def delete_filiere(
    id_filiere: UUID,
    db: Session = Depends(get_db),
    current_user: models.Utilisateur = Depends(auth.get_current_user)
):
    """Supprime une filière (Réservé Admin)."""
    if current_user.role != models.RoleUtilisateur.Admin:
        raise HTTPException(status_code=403, detail="Réservé aux administrateurs.")
    db_filiere = crud.get_filiere(db, id_filiere=id_filiere)
    if not db_filiere:
        raise HTTPException(status_code=404, detail="Filière non trouvée.")
    crud.delete_filiere(db=db, db_filiere=db_filiere)
    return None

@app.get("/categories/", response_model=List[schemas.Categorie], tags=["Administration"])
def read_categories(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Récupère la liste de toutes les catégories."""
    return crud.get_categories(db, skip=skip, limit=limit)

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

@app.put("/categories/{id_categorie}", response_model=schemas.Categorie, tags=["Administration"])
def update_categorie(
    id_categorie: UUID,
    categorie_update: schemas.CategorieUpdate,
    db: Session = Depends(get_db),
    current_user: models.Utilisateur = Depends(auth.get_current_user)
):
    """Met à jour une catégorie (Réservé Admin)."""
    if current_user.role != models.RoleUtilisateur.Admin:
        raise HTTPException(status_code=403, detail="Réservé aux administrateurs.")
    db_cat = crud.get_categorie(db, id_categorie=id_categorie)
    if not db_cat:
        raise HTTPException(status_code=404, detail="Catégorie non trouvée.")
    return crud.update_categorie(db=db, db_categorie=db_cat, categorie_update=categorie_update)

@app.delete("/categories/{id_categorie}", status_code=status.HTTP_204_NO_CONTENT, tags=["Administration"])
def delete_categorie(
    id_categorie: UUID,
    db: Session = Depends(get_db),
    current_user: models.Utilisateur = Depends(auth.get_current_user)
):
    """Supprime une catégorie (Réservé Admin)."""
    if current_user.role != models.RoleUtilisateur.Admin:
        raise HTTPException(status_code=403, detail="Réservé aux administrateurs.")
    db_cat = crud.get_categorie(db, id_categorie=id_categorie)
    if not db_cat:
        raise HTTPException(status_code=404, detail="Catégorie non trouvée.")
    try:
        crud.delete_categorie(db=db, db_categorie=db_cat)
    except Exception:
        raise HTTPException(status_code=400, detail="Impossible de supprimer une catégorie liée à des événements.")
    return None

@app.get("/lieux/", response_model=List[schemas.Lieu], tags=["Administration"])
def read_lieux(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Récupère la liste de tous les lieux."""
    return crud.get_lieux(db, skip=skip, limit=limit)

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

@app.put("/lieux/{id_lieu}", response_model=schemas.Lieu, tags=["Administration"])
def update_lieu(
    id_lieu: UUID,
    lieu_update: schemas.LieuUpdate,
    db: Session = Depends(get_db),
    current_user: models.Utilisateur = Depends(auth.get_current_user)
):
    """Met à jour un lieu (Réservé Admin)."""
    if current_user.role != models.RoleUtilisateur.Admin:
        raise HTTPException(status_code=403, detail="Réservé aux administrateurs.")
    db_lieu = crud.get_lieu(db, id_lieu=id_lieu)
    if not db_lieu:
        raise HTTPException(status_code=404, detail="Lieu non trouvé.")
    return crud.update_lieu(db=db, db_lieu=db_lieu, lieu_update=lieu_update)

@app.delete("/lieux/{id_lieu}", status_code=status.HTTP_204_NO_CONTENT, tags=["Administration"])
def delete_lieu(
    id_lieu: UUID,
    db: Session = Depends(get_db),
    current_user: models.Utilisateur = Depends(auth.get_current_user)
):
    """Supprime un lieu (Réservé Admin)."""
    if current_user.role != models.RoleUtilisateur.Admin:
        raise HTTPException(status_code=403, detail="Réservé aux administrateurs.")
    db_lieu = crud.get_lieu(db, id_lieu=id_lieu)
    if not db_lieu:
        raise HTTPException(status_code=404, detail="Lieu non trouvé.")
    try:
        crud.delete_lieu(db=db, db_lieu=db_lieu)
    except Exception:
        raise HTTPException(status_code=400, detail="Impossible de supprimer un lieu lié à des événements.")
    return None
