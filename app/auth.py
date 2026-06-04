import os
from datetime import datetime, timedelta, timezone
from pathlib import Path
from jose import jwt
from passlib.context import CryptContext
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parents[1]
load_dotenv(BASE_DIR / ".env")

# Configuration de Bcrypt pour le hachage sécurisé
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY = os.getenv("SECRET_KEY", "cle_de_secours_ultra_secrete")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

# 1. Hacher le mot de passe (utilisé dans l'inscription)
def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

# 2. Vérifier le mot de passe (utilisé dans la connexion)
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# 3. Créer le Jeton JWT
def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
