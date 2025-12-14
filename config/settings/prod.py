from .base import *
from dotenv import load_dotenv
import os

load_dotenv()

DEBUG = False
SECRET_KEY = os.getenv("SECRET_KEY")
DEBUG = os.getenv("DEBUG", "True") == "True"
ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "*").split(",")
ADMIN_URL = os.getenv("DJANGO_ADMIN_URL", "secure-admin")

DATABASES = {
    "default": {
        "ENGINE": os.getenv("DB_ENGINE", "django.db.backends.sqlite3"),
        "NAME": BASE_DIR / os.getenv("DB_NAME", "db.sqlite3"),
    }
}
