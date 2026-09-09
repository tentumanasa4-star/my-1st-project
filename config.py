import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "campus_events_super_secret_key_2026_jwt_token")
    JWT_SECRET = os.getenv("JWT_SECRET", "campus_events_jwt_secret_token_secure_key_512")
    JWT_EXPIRATION_HOURS = int(os.getenv("JWT_EXPIRATION_HOURS", "24"))
    
    # MongoDB connection details
    MONGODB_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
    DATABASE_NAME = os.getenv("DATABASE_NAME", "campus_events_db")
    
    # Fallback data directory if MongoDB server is unavailable
    DATA_DIR = os.getenv("DATA_DIR", str(BASE_DIR / "data"))
