import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

"""
Ce module gère la configuration de la base de données SQLAlchemy.
Il charge les variables d'environnement et initialise la connexion à PostgreSQL.
"""

# Chargement des variables d'environnement depuis le fichier .env
load_dotenv()

# URL de connexion à la base de données (PostgreSQL)
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

# Création de l'engine SQLAlchemy
# L'engine est le point de départ de toute application SQLAlchemy
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Création d'une classe de session locale
# Chaque instance de SessionLocal sera une session de base de données réelle
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base de classe pour les modèles ORM
Base = declarative_base()

def get_db():
    """
    Dépendance pour obtenir une session de base de données.
    Assure que la session est fermée après l'utilisation.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
