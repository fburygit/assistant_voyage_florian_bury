# Assistant Voyage

Petit projet d'API pour préparer un voyage.

L'application permet de :

- créer un compte utilisateur ;
- se connecter avec un token JWT ;
- demander une proposition de voyage pour une ville ;
- récupérer la météo de la ville ;
- afficher quelques activités depuis la base de données.

## Structure du projet

```text
assistant_voyage/
├── app/
│   ├── main.py       # routes FastAPI
│   ├── database.py   # connexion MySQL
│   ├── models.py     # tables SQLAlchemy
│   ├── schemas.py    # modèles Pydantic
│   └── auth.py       # mots de passe et JWT
├── frontend/
│   └── index.html    # interface web
├── tests/
│   ├── test_initial.py
│   └── test_connexion_db.py
├── main.py           # point d'entrée simple
├── requirements.txt
└── .env
```

## Installation

Depuis le dossier `assistant_voyage` :

```powershell
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

## Configuration

Le fichier `.env` doit contenir les informations de connexion à la base MySQL et la clé météo.

Exemple :

```env
DB_USER=root
DB_PASSWORD=
DB_HOST=127.0.0.1
DB_PORT=3306
DB_NAME=assistant_voyage_db

METEO_API_KEY=ta_cle_openweather
SECRET_KEY=une_cle_secrete
```

Avant de lancer l'API, il faut aussi vérifier que MySQL est démarré et que la base `assistant_voyage_db` existe.

## Lancer l'API

Depuis `assistant_voyage` :

```powershell
venv\Scripts\uvicorn.exe app.main:app --reload
```

L'API sera disponible ici :

```text
http://127.0.0.1:8000
```

La documentation FastAPI est disponible ici :

```text
http://127.0.0.1:8000/docs
```

## Interface web

Le fichier HTML se trouve dans :

```text
frontend/index.html
```

Il utilise l'API locale sur `http://127.0.0.1:8000`.

## Tests utiles

Pour vérifier la configuration de départ :

```powershell
venv\Scripts\python.exe tests\test_initial.py
```

Pour vérifier la connexion à la base et créer les tables :

```powershell
venv\Scripts\python.exe tests\test_connexion_db.py
```

## Routes principales

- `POST /signup` : créer un utilisateur
- `POST /login` : se connecter
- `GET /users` : lister les utilisateurs
- `POST /plan` : obtenir une proposition de voyage pour une ville

## Notes

Le projet utilise MySQL, donc XAMPP ou un serveur MySQL doit être lancé avant les tests liés à la base.

La route `/plan` utilise OpenWeather, il faut donc une clé API valide dans le fichier `.env`.
