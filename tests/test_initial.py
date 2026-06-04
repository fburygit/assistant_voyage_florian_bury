import os
from pathlib import Path
import requests
from dotenv import load_dotenv
import mysql.connector

# 1. Chargement du fichier .env
BASE_DIR = Path(__file__).resolve().parents[1]
load_dotenv(BASE_DIR / ".env")

print("--- 1. VÉRIFICATION DU FICHIER .ENV ---")
print(f"Base de données : {os.getenv('DB_NAME')}")
print(f"Clé Météo configurée : {'Oui' if os.getenv('METEO_API_KEY') else 'Non'}")

print("\n--- 2. TEST DE CONNEXION À MYSQL ---")
try:
    conn = mysql.connector.connect(
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        database=os.getenv("DB_NAME")
    )
    print("✅ Connexion à la base de données MySQL réussie !")
    conn.close()
except Exception as e:
    print(f"❌ Échec de la connexion MySQL. Erreur : {e}")
    print("💡 Conseil : Assure-toi d'avoir créé la base vide 'assistant_voyage_db' dans MySQL.")

print("\n--- 3. TEST DE L'API MÉTÉO (OPENWEATHER) ---")
ville_test = "Paris"
api_key = os.getenv("METEO_API_KEY")

if api_key:
    url = f"https://api.openweathermap.org/data/2.5/weather?q={ville_test}&appid={api_key}&units=metric&lang=fr"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            temp = data["main"]["temp"]
            desc = data["weather"][0]["description"]
            print(f"✅ API Météo fonctionnelle ! À {ville_test}, il fait {temp}°C avec des conditions de type : '{desc}'.")
        else:
            print(f"❌ Erreur API Météo (Code {response.status_code}) : {response.json().get('message')}")
    except Exception as e:
        print(f"❌ Impossible de joindre l'API Météo : {e}")
else:
    print("❌ Clé API Météo manquante dans le fichier .env")
