from pydantic import BaseModel, EmailStr, Field
from datetime import date

# Ce que Postman doit envoyer pour inscrire un utilisateur
class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=6, description="Le mot de passe doit faire au moins 6 caractères")
    nom: str = Field(..., min_length=2)
    prenom: str = Field(..., min_length=2)
    date_naissance: date # Format attendu : AAAA-MM-JJ

# Ce que l'API renvoie après une inscription réussie
class UserResponse(BaseModel):
    id: int
    email: EmailStr
    nom: str
    prenom: str
    date_naissance: date

    class Config:
        from_attributes = True

# Ce que Postman enverra pour la planification d'un voyage 
class PlanRequest(BaseModel):
    city: str