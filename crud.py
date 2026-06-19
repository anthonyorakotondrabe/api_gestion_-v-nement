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

def get_utilisateurs(db: Session, skip: int = 0, limit: int = 100):
    """
    Récupère la liste de tous les utilisateurs avec pagination.
    """
    return db.query(models.Utilisateur).offset(skip).limit(limit).all()

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

def update_utilisateur(db: Session, db_user: models.Utilisateur, user_update: schemas.UtilisateurUpdate):
    """
    Met à jour les informations d'un utilisateur.
    """
    update_data = user_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_user, key, value)

    db.commit()
    db.refresh(db_user)
    return db_user

def delete_utilisateur(db: Session, db_user: models.Utilisateur):
    """
    Supprime un utilisateur de la base de données.
    """
    db.delete(db_user)
    db.commit()
    return True

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

def get_inscriptions_by_user(db: Session, id_utilisateur: UUID):
    """
    Récupère toutes les inscriptions d'un utilisateur donné.
    """
    return db.query(models.Inscription).filter(models.Inscription.id_utilisateur == id_utilisateur).all()

def get_inscriptions_by_event(db: Session, id_evenement: UUID):
    """
    Récupère tous les inscrits à un événement donné.
    """
    return db.query(models.Inscription).filter(models.Inscription.id_evenement == id_evenement).all()

def get_inscription_by_id(db: Session, id_inscription: UUID):
    """
    Récupère une inscription par son ID.
    """
    return db.query(models.Inscription).filter(models.Inscription.id_inscription == id_inscription).first()

def delete_inscription(db: Session, db_inscription: models.Inscription):
    """
    Supprime une inscription.
    """
    db.delete(db_inscription)
    db.commit()
    return True

# --- Fonctions de Référence (Filiere, Categorie, Lieu) ---

def get_filiere(db: Session, id_filiere: UUID):
    """Récupère une filière par son ID."""
    return db.query(models.Filiere).filter(models.Filiere.id_filiere == id_filiere).first()

def get_filieres(db: Session, skip: int = 0, limit: int = 100):
    """Récupère la liste des filières."""
    return db.query(models.Filiere).offset(skip).limit(limit).all()

def create_filiere(db: Session, filiere: schemas.FiliereCreate):
    """Crée une nouvelle filière."""
    db_filiere = models.Filiere(**filiere.model_dump())
    db.add(db_filiere)
    db.commit()
    db.refresh(db_filiere)
    return db_filiere

def update_filiere(db: Session, db_filiere: models.Filiere, filiere_update: schemas.FiliereUpdate):
    """Met à jour une filière."""
    update_data = filiere_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_filiere, key, value)
    db.commit()
    db.refresh(db_filiere)
    return db_filiere

def delete_filiere(db: Session, db_filiere: models.Filiere):
    """Supprime une filière."""
    db.delete(db_filiere)
    db.commit()
    return True

def get_categorie(db: Session, id_categorie: UUID):
    """Récupère une catégorie par son ID."""
    return db.query(models.Categorie).filter(models.Categorie.id_categorie == id_categorie).first()

def get_categories(db: Session, skip: int = 0, limit: int = 100):
    """Récupère la liste des catégories."""
    return db.query(models.Categorie).offset(skip).limit(limit).all()

def create_categorie(db: Session, categorie: schemas.CategorieCreate):
    """Crée une nouvelle catégorie d'événement."""
    db_cat = models.Categorie(**categorie.model_dump())
    db.add(db_cat)
    db.commit()
    db.refresh(db_cat)
    return db_cat

def update_categorie(db: Session, db_categorie: models.Categorie, categorie_update: schemas.CategorieUpdate):
    """Met à jour une catégorie."""
    update_data = categorie_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_categorie, key, value)
    db.commit()
    db.refresh(db_categorie)
    return db_categorie

def delete_categorie(db: Session, db_categorie: models.Categorie):
    """Supprime une catégorie."""
    db.delete(db_categorie)
    db.commit()
    return True

def get_lieu(db: Session, id_lieu: UUID):
    """Récupère un lieu par son ID."""
    return db.query(models.Lieu).filter(models.Lieu.id_lieu == id_lieu).first()

def get_lieux(db: Session, skip: int = 0, limit: int = 100):
    """Récupère la liste des lieux."""
    return db.query(models.Lieu).offset(skip).limit(limit).all()

def create_lieu(db: Session, lieu: schemas.LieuCreate):
    """Crée un nouveau lieu."""
    db_lieu = models.Lieu(**lieu.model_dump())
    db.add(db_lieu)
    db.commit()
    db.refresh(db_lieu)
    return db_lieu

def update_lieu(db: Session, db_lieu: models.Lieu, lieu_update: schemas.LieuUpdate):
    """Met à jour un lieu."""
    update_data = lieu_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_lieu, key, value)
    db.commit()
    db.refresh(db_lieu)
    return db_lieu

def delete_lieu(db: Session, db_lieu: models.Lieu):
    """Supprime un lieu."""
    db.delete(db_lieu)
    db.commit()
    return True
