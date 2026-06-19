from sqlalchemy.orm import Session
from uuid import UUID
import models, schemas, auth

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

def get_utilisateur_by_email(db: Session, email: str):
    """
    Récupère un utilisateur par son email.
    """
    return db.query(models.Utilisateur).filter(models.Utilisateur.email == email).first()

def create_utilisateur(db: Session, utilisateur: schemas.UtilisateurCreate):
    """
    Crée un nouvel utilisateur avec mot de passe haché.
    """
    hashed_password = auth.get_password_hash(utilisateur.password)

    # On retire le mot de passe en clair et on gère l'ID optionnel
    user_data = utilisateur.model_dump(exclude={"password"})
    if user_data.get("id_utilisateur") is None:
        user_data.pop("id_utilisateur")

    db_user = models.Utilisateur(**user_data, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# --- Evenement ---

def get_evenement(db: Session, id_evenement: UUID):
    """
    Récupère un événement spécifique par son ID.
    """
    return db.query(models.Evenement).filter(models.Evenement.id_evenement == id_evenement).first()

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

def update_evenement(db: Session, db_evenement: models.Evenement, evenement_update: schemas.EvenementUpdate):
    """
    Met à jour un événement existant.
    """
    update_data = evenement_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_evenement, key, value)

    db.commit()
    db.refresh(db_evenement)
    return db_evenement

def delete_evenement(db: Session, db_evenement: models.Evenement):
    """
    Supprime un événement.
    """
    db.delete(db_evenement)
    db.commit()
    return True

# --- Inscription ---

def get_inscription(db: Session, id_evenement: UUID, id_utilisateur: UUID):
    """
    Vérifie si un utilisateur est déjà inscrit à un événement.
    """
    return db.query(models.Inscription).filter(
        models.Inscription.id_evenement == id_evenement,
        models.Inscription.id_utilisateur == id_utilisateur
    ).first()

def count_inscriptions_evenement(db: Session, id_evenement: UUID):
    """
    Compte le nombre total d'inscriptions confirmées pour un événement donné.
    """
    return db.query(models.Inscription).filter(
        models.Inscription.id_evenement == id_evenement,
        models.Inscription.statut_inscription != models.StatutInscription.Annule
    ).count()

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
