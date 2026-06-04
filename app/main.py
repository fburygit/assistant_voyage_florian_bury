from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import List # Import nécessaire pour lister plusieurs éléments
import requests
from app.database import get_db, engine, Base
from app import models, schemas, auth
from fastapi.middleware.cors import CORSMiddleware

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Assistant de Planification de Voyage")

# --- AJOUT DE LA SÉCURITÉ CORS POUR L'INTERFACE ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"],
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

@app.get("/")
def home():
    return {"message": "Bienvenue sur l'API de l'Assistant de Voyage !"}


# ==========================================
# 1. INSCRIPTION : Changé en /signup 
# ==========================================
@app.post("/signup", response_model=schemas.UserResponse, status_code=status.HTTP_201_CREATED)
def inscription(user_in: schemas.UserCreate, db: Session = Depends(get_db)):
    user_existant = db.query(models.User).filter(models.User.email == user_in.email).first()
    if user_existant:
        raise HTTPException(status_code=400, detail="Cet e-mail est déjà utilisé.")
    
    mot_de_passe_hache = auth.get_password_hash(user_in.password)
    
    nouvel_utilisateur = models.User(
        email=user_in.email,
        hashed_password=mot_de_passe_hache,
        nom=user_in.nom,
        prenom=user_in.prenom,
        date_naissance=user_in.date_naissance
    )
    db.add(nouvel_utilisateur)
    db.commit()
    db.refresh(nouvel_utilisateur)
    return nouvel_utilisateur


# ==========================================
# LISTER LES UTILISATEURS (GET /users)
# ==========================================
@app.get("/users", response_model=List[schemas.UserResponse])
def lister_utilisateurs(db: Session = Depends(get_db)):
    utilisateurs = db.query(models.User).all()
    return utilisateurs


# ==========================================
# 2. CONNEXION (POST /login) 
# ==========================================
@app.post("/login")
def connexion(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == form_data.username).first()
    if not user or not auth.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou mot de passe incorrect.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = auth.create_access_token(data={"sub": user.email, "user_id": user.id})
    return {"access_token": access_token, "token_type": "bearer"}


# ==========================================
# 3. PLANIFICATION (POST /plan) 
# ==========================================
@app.post("/plan")
def planifier_voyage(plan_in: schemas.PlanRequest, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    import os
    
    ville = plan_in.city.strip()
    api_key = os.getenv("METEO_API_KEY")
    
    # 1. APPEL METEO (Directement sur Internet)
    url_meteo = f"https://api.openweathermap.org/data/2.5/weather?q={ville}&appid={api_key}&units=metric&lang=fr"
    try:
        reponse_meteo = requests.get(url_meteo)
        if reponse_meteo.status_code != 200:
            raise HTTPException(status_code=404, detail=f"Impossible de trouver la météo pour la ville : {ville}")
        data_meteo = reponse_meteo.json()
        meteo_propre = {
            "temperature": f"{data_meteo['main']['temp']}°C",
            "conditions": data_meteo['weather'][0]['description'],
            "icone": data_meteo['weather'][0]['icon']
        }
    except Exception:
        raise HTTPException(status_code=502, detail="Erreur avec le service météo externe.")

    # 2. APPEL BDD 
    # On cherche dans la table 'Evenement' les lignes où lieu_ville correspond exactement
    evenements_bdd = db.query(models.Evenement).filter(models.Evenement.lieu_ville.ilike(f"%{ville}%")).all()
       
    # On extrait uniquement le nom de chaque événement trouvé
    activites = [evt.nom_evenement for evt in evenements_bdd]
    
    # 3. MESSAGE DE SECOURS (Si la ville n'existe pas du tout dans ton phpMyAdmin)
    if not activites:
        activites = [
            "Faire une visite guidée du centre-ville",
            "Goûter les spécialités culinaires locales",
            "Se balader dans les rues historiques"
        ]

    # 4. ENVOI DES DONNÉES COMBINÉES
    return {
        "ville": ville,
        "meteo": meteo_propre,
        "activites_recommandees": activites
    }
