import os
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "troque-esta-chave-no-env")
    MAX_CONTENT_LENGTH = 5 * 1024 * 1024  # 5 MB
    UPLOAD_FOLDER = os.path.join(BASE_DIR, "static")
    DATABASE_PATH = os.path.join(BASE_DIR, "banco.db")

    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SECURE   = True
    SESSION_COOKIE_SAMESITE = "Lax"

    ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "webp"}

    # Rate limiting
    DEFAULT_LIMITS = ["200 per day", "50 per hour"]