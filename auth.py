import os
import hashlib
from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from database import get_db
import crud, models, schemas

"""
Ce module gère la sécurité : hachage des mots de passe et gestion des tokens JWT.
Il inclut un pré-hachage SHA-256 pour contourner la limite de 72 caractères de Bcrypt.
"""

# Configuration pour le hachage des mots de passe
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Configuration JWT
SECRET_KEY = os.getenv("SECRET_KEY", "une_cle_secrete_tres_longue_et_aleatoire_123456789")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24  # Le token expire après 24 heures

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

def verify_password(plain_password, hashed_password):
    """
    Vérifie si le mot de passe en clair correspond au hash.
    Applique SHA-256 en amont pour la compatibilité avec Bcrypt.
    """
    sha256_password = hashlib.sha256(plain_password.encode('utf-8')).hexdigest()
    return pwd_context.verify(sha256_password, hashed_password)

def get_password_hash(password):
    """
    Génère un hash sécurisé pour le mot de passe.
    Applique SHA-256 pour contourner la limite de 72 caractères de Bcrypt.
    """
    sha256_password = hashlib.sha256(password.encode('utf-8')).hexdigest()
    return pwd_context.hash(sha256_password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Génère un token JWT signé."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    """
    Dépendance pour récupérer l'utilisateur actuellement connecté via son token JWT.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Impossible de valider les identifiants",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = crud.get_utilisateur(db, id_utilisateur=user_id)
    if user is None:
        raise credentials_exception
    return user
