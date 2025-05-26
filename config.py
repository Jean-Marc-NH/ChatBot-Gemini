import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent


API_KEY = os.getenv("GEMINI_API_KEY")

GEMINI_API_KEY = API_KEY
USERS_DIR = BASE_DIR / "Usuarios"
MEMORY_DIR = BASE_DIR / "memoria"
MEMORY_DIR.mkdir(exist_ok=True)
MEMORY_FILE = MEMORY_DIR / "ligera.json"

SPOTIPY_CLIENT_ID = os.getenv("SPOTIPY_CLIENT_ID", "")
SPOTIPY_CLIENT_SECRET = os.getenv("SPOTIPY_CLIENT_SECRET", "")
SPOTIPY_REDIRECT_URI = os.getenv("SPOTIPY_REDIRECT_URI", "")


STT_CONFIG = {
    "language": "es-ES", 
    "energy_threshold": 300,
    "pause_threshold": 0.8,
}

TTS_CONFIG = {
    "rate": 150, 
    "volume": 1.0,
}

GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.0-flash")


SESSION_MAX_TURNS = int(os.getenv("SESSION_MAX_TURNS", 10))  

EXIT_PHRASES = {"salir", "chau", "terminar", "adios"}
