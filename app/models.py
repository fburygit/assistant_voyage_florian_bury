from sqlalchemy import Column, Integer, String, Date
from app.database import Base

# Table Utilisateur (email, mot de passe, nom, prénom, date de naissance)
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    nom = Column(String(100), nullable=False)
    prenom = Column(String(100), nullable=False)
    date_naissance = Column(Date, nullable=False)

# Table Événement (identifiant, nom de l'événement, date, lieu surtout la ville)
class Evenement(Base):
    __tablename__ = "evenements"

    id = Column(Integer, primary_key=True, index=True)
    nom_evenement = Column(String(255), nullable=False)
    date = Column(Date, nullable=False)
    lieu_ville = Column(String(150), index=True, nullable=False)
