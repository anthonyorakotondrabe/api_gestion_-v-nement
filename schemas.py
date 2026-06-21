from pydantic import BaseModel, EmailStr, ConfigDict
from typing import List, Optional
from datetime import datetime
from uuid import UUID
from decimal import Decimal
from models import RoleUtilisateur, StatutEvenement, StatutInscription

"""
Ce module définit les schémas Pydantic pour la validation des données.
Ils sont utilisés pour les entrées (requêtes) et les sorties (réponses) de l'API.
"""

# --- AUTHENTIFICATION ---

class Token(BaseModel):
    """Schéma pour le token JWT retourné après connexion."""
    access_token: str
    token_type: str

class TokenData(BaseModel):
    """Schéma pour les données contenues dans le token."""
    id_utilisateur: Optional[str] = None

# --- FILIERE ---

class FiliereBase(BaseModel):
    """Schéma de base pour une Filière."""
    nom_filiere: str

class FiliereCreate(FiliereBase):
    """Schéma pour la création d'une Filière."""
    pass

class FiliereUpdate(BaseModel):
    """Schéma pour la mise à jour d'une Filière."""
    nom_filiere: Optional[str] = None

class Filiere(FiliereBase):
    """Schéma complet représentant une Filière en sortie de l'API."""
    id_filiere: UUID
    model_config = ConfigDict(from_attributes=True)

# --- CATEGORIE ---

class CategorieBase(BaseModel):
    """Schéma de base pour une Catégorie."""
    libelle: str

class CategorieCreate(CategorieBase):
    """Schéma pour la création d'une Catégorie."""
    pass

class CategorieUpdate(BaseModel):
    """Schéma pour la mise à jour d'une Catégorie."""
    libelle: Optional[str] = None

class Categorie(CategorieBase):
    """Schéma complet représentant une Catégorie en sortie de l'API."""
    id_categorie: UUID
    model_config = ConfigDict(from_attributes=True)

# --- LIEU ---

class LieuBase(BaseModel):
    """Schéma de base pour un Lieu."""
    nom_lieu: str
    adresse: Optional[str] = None
    ville: Optional[str] = None
    code_postal: Optional[str] = None

class LieuCreate(LieuBase):
    """Schéma pour la création d'un Lieu."""
    pass

class LieuUpdate(BaseModel):
    """Schéma pour la mise à jour d'un Lieu."""
    nom_lieu: Optional[str] = None
    adresse: Optional[str] = None
    ville: Optional[str] = None
    code_postal: Optional[str] = None

class Lieu(LieuBase):
    """Schéma complet représentant un Lieu en sortie de l'API."""
    id_lieu: UUID
    model_config = ConfigDict(from_attributes=True)

# --- UTILISATEUR ---

class UtilisateurBase(BaseModel):
    """Schéma de base pour un Utilisateur."""
    nom: str
    email: EmailStr
    role: RoleUtilisateur = RoleUtilisateur.Etudiant
    id_filiere: Optional[UUID] = None

class UtilisateurCreate(UtilisateurBase):
    """Schéma pour la création d'un Utilisateur."""
    id_utilisateur: Optional[UUID] = None
    password: str

class UtilisateurUpdate(BaseModel):
    """Schéma pour la mise à jour d'un Utilisateur par un Admin."""
    nom: Optional[str] = None
    email: Optional[EmailStr] = None
    role: Optional[RoleUtilisateur] = None
    id_filiere: Optional[UUID] = None

class Utilisateur(UtilisateurBase):
    """Schéma complet représentant un Utilisateur en sortie de l'API."""
    id_utilisateur: UUID
    model_config = ConfigDict(from_attributes=True)

# --- EVENEMENT ---

class EvenementBase(BaseModel):
    """Schéma de base pour un Événement."""
    titre: str
    description: Optional[str] = None
    date_evenement: datetime
    prix: Decimal = Decimal("0.0")
    capacite_max: int
    statut_evenement: StatutEvenement = StatutEvenement.Brouillon
    id_categorie: UUID
    id_lieu: UUID

class EvenementCreate(EvenementBase):
    """Schéma pour la création d'un Événement."""
    pass

class EvenementUpdate(BaseModel):
    """Schéma pour la mise à jour partielle d'un Événement."""
    titre: Optional[str] = None
    description: Optional[str] = None
    date_evenement: Optional[datetime] = None
    prix: Optional[Decimal] = None
    capacite_max: Optional[int] = None
    statut_evenement: Optional[StatutEvenement] = None
    id_categorie: Optional[UUID] = None
    id_lieu: Optional[UUID] = None

class Evenement(EvenementBase):
    """Schéma complet représentant un Événement en sortie de l'API."""
    id_evenement: UUID
    createur_id: UUID
    date_creation: datetime
    model_config = ConfigDict(from_attributes=True)

# --- INSCRIPTION ---

class InscriptionBase(BaseModel):
    """Schéma de base pour une Inscription."""
    id_evenement: UUID

class InscriptionCreate(InscriptionBase):
    """Schéma pour la création d'une Inscription."""
    pass

class Inscription(InscriptionBase):
    """Schéma complet représentant une Inscription en sortie de l'API."""
    id_inscription: UUID
    id_utilisateur: UUID
    date_inscription: datetime
    statut_inscription: StatutInscription
    model_config = ConfigDict(from_attributes=True)

class InscriptionUpdate(BaseModel):
    """Schéma pour la mise à jour d'une Inscription."""
    statut_inscription: Optional[StatutInscription] = None
