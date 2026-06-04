import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from app.database import engine, Base
from app import models

print("⏳ Tentative de connexion à MySQL et création des tables...")

try:
    # Test de connexion et génération des tables users et evenements
    Base.metadata.create_all(bind=engine)
    print("✅ Connexion à la base de données MySQL réussie !")
    print("🏆 Les tables 'users' et 'evenements' ont été générées avec succès dans phpMyAdmin !")
except Exception as e:
    print(f"❌ Échec de la connexion. Erreur technique : {e}")
    print("💡 Conseil : Vérifie que XAMPP (Apache + MySQL) est bien vert et que ta base vide 'assistant_voyage_db' existe.")
