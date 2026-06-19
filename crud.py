from sqlalchemy.orm import Session
from uuid import UUID
import models, schemas

"""
Ce module regroupe les fonctions CRUD (Create, Read, Update, Delete).
Il assure l'interface entre les schémas Pydantic et les modèles SQLAlchemy.
"""

# --- Utilisateur ---

def get_utilisateur(db: Session, id_utilisateur: UUID):
    """
    Récupère un utilisateur par son identifiant unique.
    """
    return db.query(models.Utilisateur).filter(models.Utilisateur.id_utilisateur == id_utilisateur).first()

def create_utilisateur(db: Session, utilisateur: schemas.UtilisateurCreate):
    """
    Crée un nouvel utilisateur dans la base de données.
    """
    db_user = models.Utilisateur(**utilisateur.model_dump())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# --- Evenement ---

def get_evenements(db: Session, skip: int = 0, limit: int = 100):
    """
    Récupère la liste des événements avec pagination.
    """
    return db.query(models.Evenement).offset(skip).limit(limit).all()

def create_evenement(db: Session, evenement: schemas.EvenementCreate, createur_id: UUID):
    """
    Crée un nouvel événement associé à un créateur.
    """
    db_event = models.Evenement(**evenement.model_dump(), createur_id=createur_id)
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return db_event

# --- Inscription ---

def create_inscription(db: Session, id_evenement: UUID, id_utilisateur: UUID):
    """
    Enregistre l'inscription d'un utilisateur à un événement.
    """
    db_inscription = models.Inscription(id_evenement=id_evenement, id_utilisateur=id_utilisateur)
    db.add(db_inscription)
    db.commit()
    db.refresh(db_inscription)
    return db_inscription

# --- Fonctions de Référence (Filiere, Categorie, Lieu) ---

def create_filiere(db: Session, filiere: schemas.FiliereCreate):
    """Crée une nouvelle filière."""
    db_filiere = models.Filiere(**filiere.model_dump())
    db.add(db_filiere)
    db.commit()
    db.refresh(db_filiere)
    return db_filiere

def create_categorie(db: Session, categorie: schemas.CategorieCreate):
    """Crée une nouvelle catégorie d'événement."""
    db_cat = models.Categorie(**categorie.model_dump())
    db.add(db_cat)
    db.commit()
    db.refresh(db_cat)
    return db_cat

def create_lieu(db: Session, lieu: schemas.LieuCreate):
    """Crée un nouveau lieu."""
    db_lieu = models.Lieu(**lieu.model_dump())
    db.add(db_lieu)
    db.commit()
    db.refresh(db_lieu)
    return db_lieu
