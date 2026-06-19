import uuid
import enum
from sqlalchemy import Column, String, DateTime, ForeignKey, Text, Numeric, Integer, Enum, Table
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base

"""
Ce module définit les modèles SQLAlchemy (ORM) correspondant au schéma de la base de données.
Il utilise des types UUID pour les identifiants et des Enums PostgreSQL pour les statuts et rôles.
"""

# --- Énumérations (Enums) ---

class RoleUtilisateur(str, enum.Enum):
    """Rôles possibles pour un utilisateur au sein du système."""
    Etudiant = "Etudiant"
    Organisateur = "Organisateur"
    Admin = "Admin"

class StatutEvenement(str, enum.Enum):
    """Différents états d'un événement."""
    Brouillon = "Brouillon"
    Publie = "Publié"
    Annule = "Annulé"
    Passe = "Passé"

class StatutInscription(str, enum.Enum):
    """Statuts possibles pour une inscription d'un étudiant à un événement."""
    EnAttente = "En attente"
    Confirme = "Confirmé"
    Annule = "Annulé"

# --- Table de jointure ---

# Table de jointure Many-to-Many entre Evenement et Filiere
evenement_filiere = Table(
    "evenement_filiere",
    Base.metadata,
    Column("id_evenement", UUID(as_uuid=True), ForeignKey("evenement.id_evenement", ondelete="CASCADE"), primary_key=True),
    Column("id_filiere", UUID(as_uuid=True), ForeignKey("filiere.id_filiere", ondelete="CASCADE"), primary_key=True),
)

# --- Modèles de Tables ---

class Filiere(Base):
    """Modèle représentant une filière universitaire (ex: Informatique, Gestion)."""
    __tablename__ = "filiere"
    id_filiere = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nom_filiere = Column(String, nullable=False)

    # Relations
    utilisateurs = relationship("Utilisateur", back_populates="filiere")
    evenements = relationship("Evenement", secondary=evenement_filiere, back_populates="filieres")

class Categorie(Base):
    """Catégorie thématique d'un événement (ex: Conférence, Atelier, Sport)."""
    __tablename__ = "categorie"
    id_categorie = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    libelle = Column(String, nullable=False)

    # Relations
    evenements = relationship("Evenement", back_populates="categorie")

class Lieu(Base):
    """Emplacement physique d'un événement."""
    __tablename__ = "lieu"
    id_lieu = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nom_lieu = Column(String, nullable=False)
    adresse = Column(String)
    ville = Column(String)
    code_postal = Column(String)

    # Relations
    evenements = relationship("Evenement", back_populates="lieu")

class Utilisateur(Base):
    """
    Modèle représentant un utilisateur du système.
    L'id_utilisateur est lié à l'ID généré par Supabase Auth.
    """
    __tablename__ = "utilisateur"
    id_utilisateur = Column(UUID(as_uuid=True), primary_key=True)
    nom = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    role = Column(Enum(RoleUtilisateur), default=RoleUtilisateur.Etudiant)
    id_filiere = Column(UUID(as_uuid=True), ForeignKey("filiere.id_filiere", ondelete="SET NULL"))

    # Relations
    filiere = relationship("Filiere", back_populates="utilisateurs")
    evenements_crees = relationship("Evenement", back_populates="createur")
    inscriptions = relationship("Inscription", back_populates="utilisateur")

class Evenement(Base):
    """Modèle représentant un événement universitaire."""
    __tablename__ = "evenement"
    id_evenement = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    titre = Column(String, nullable=False)
    description = Column(Text)
    date_evenement = Column(DateTime(timezone=True), nullable=False)
    date_creation = Column(DateTime(timezone=True), server_default=func.now())
    prix = Column(Numeric, default=0)
    capacite_max = Column(Integer, nullable=False)
    statut_evenement = Column(Enum(StatutEvenement), default=StatutEvenement.Brouillon)
    createur_id = Column(UUID(as_uuid=True), ForeignKey("utilisateur.id_utilisateur", ondelete="CASCADE"), nullable=False)
    id_categorie = Column(UUID(as_uuid=True), ForeignKey("categorie.id_categorie", ondelete="RESTRICT"), nullable=False)
    id_lieu = Column(UUID(as_uuid=True), ForeignKey("lieu.id_lieu", ondelete="RESTRICT"), nullable=False)

    # Relations
    createur = relationship("Utilisateur", back_populates="evenements_crees")
    categorie = relationship("Categorie", back_populates="evenements")
    lieu = relationship("Lieu", back_populates="evenements")
    filieres = relationship("Filiere", secondary=evenement_filiere, back_populates="evenements")
    inscriptions = relationship("Inscription", back_populates="evenement")

class Inscription(Base):
    """Modèle représentant l'inscription d'un utilisateur à un événement."""
    __tablename__ = "inscription"
    id_inscription = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    date_inscription = Column(DateTime(timezone=True), server_default=func.now())
    statut_inscription = Column(Enum(StatutInscription), default=StatutInscription.EnAttente)
    id_utilisateur = Column(UUID(as_uuid=True), ForeignKey("utilisateur.id_utilisateur", ondelete="CASCADE"), nullable=False)
    id_evenement = Column(UUID(as_uuid=True), ForeignKey("evenement.id_evenement", ondelete="CASCADE"), nullable=False)

    # Relations
    utilisateur = relationship("Utilisateur", back_populates="inscriptions")
    evenement = relationship("Evenement", back_populates="inscriptions")
