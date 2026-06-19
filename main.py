from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

import models, schemas, crud
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
    description="API pour la gestion des événements universitaires avec intégration Supabase."
)

@app.get("/")
def read_root():
    """Route d'accueil de l'API."""
    return {"message": "Bienvenue sur l'API de gestion d'événements universitaires"}

# --- Routes Utilisateurs ---

@app.post("/utilisateurs/", response_model=schemas.Utilisateur, tags=["Utilisateurs"])
def create_user(utilisateur: schemas.UtilisateurCreate, db: Session = Depends(get_db)):
    """Crée un nouvel utilisateur (L'UUID doit provenir de Supabase Auth)."""
    db_user = crud.get_utilisateur(db, id_utilisateur=utilisateur.id_utilisateur)
    if db_user:
        raise HTTPException(status_code=400, detail="L'utilisateur existe déjà.")
    return crud.create_utilisateur(db=db, utilisateur=utilisateur)

# --- Routes Événements ---

@app.get("/evenements/", response_model=List[schemas.Evenement], tags=["Événements"])
def read_evenements(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Récupère la liste de tous les événements."""
    return crud.get_evenements(db, skip=skip, limit=limit)

@app.post("/utilisateurs/{createur_id}/evenements/", response_model=schemas.Evenement, tags=["Événements"])
def create_evenement(
    createur_id: UUID, evenement: schemas.EvenementCreate, db: Session = Depends(get_db)
):
    """Crée un événement associé à un utilisateur organisateur."""
    return crud.create_evenement(db=db, evenement=evenement, createur_id=createur_id)

# --- Routes Inscriptions ---

@app.post("/evenements/{id_evenement}/inscrire/{id_utilisateur}", response_model=schemas.Inscription, tags=["Inscriptions"])
def register_for_event(id_evenement: UUID, id_utilisateur: UUID, db: Session = Depends(get_db)):
    """Inscrit un utilisateur à un événement spécifique."""
    return crud.create_inscription(db=db, id_evenement=id_evenement, id_utilisateur=id_utilisateur)

# --- Routes de Référence (Administration) ---

@app.post("/filieres/", response_model=schemas.Filiere, tags=["Administration"])
def create_filiere(filiere: schemas.FiliereCreate, db: Session = Depends(get_db)):
    """Crée une nouvelle filière universitaire."""
    return crud.create_filiere(db=db, filiere=filiere)

@app.post("/categories/", response_model=schemas.Categorie, tags=["Administration"])
def create_categorie(categorie: schemas.CategorieCreate, db: Session = Depends(get_db)):
    """Crée une nouvelle catégorie d'événement."""
    return crud.create_categorie(db=db, categorie=categorie)

@app.post("/lieux/", response_model=schemas.Lieu, tags=["Administration"])
def create_lieu(lieu: schemas.LieuCreate, db: Session = Depends(get_db)):
    """Crée un nouveau lieu pour les événements."""
    return crud.create_lieu(db=db, lieu=lieu)
