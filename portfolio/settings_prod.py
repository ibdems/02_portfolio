import os

import dj_database_url
import environ

from .settings import *  # noqa  # Importe toutes les configurations de base depuis le fichier settings.py

# Initialisation de l'objet pour lire les variables d'environnement
env = environ.Env(
    DEBUG=(bool, False)  # Par défaut, DEBUG est défini comme un booléen et désactivé (False)
)

# Définition du répertoire de base du projet
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Lecture des variables d'environnement à partir du fichier .env
environ.Env.read_env(os.path.join(BASE_DIR, ".env"))

# Clé secrète pour sécuriser Django
SECRET_KEY = env("SECRET_KEY")

# Mode DEBUG (désactivé en production pour des raisons de sécurité)
DEBUG = env("DEBUG")

# Hôtes autorisés à accéder à l'application
ALLOWED_HOSTS = env("ALLOWED_HOSTS").split(",")

# Configuration de la base de données
DATABASES = {"default": dj_database_url.config(conn_health_checks=True)}

# AWS Credentials
AWS_ACCESS_KEY_ID = env("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = env("AWS_SECRET_ACCESS_KEY")
AWS_STORAGE_BUCKET_NAME = env("AWS_STORAGE_BUCKET_NAME")
AWS_S3_REGION_NAME = "eu-west-3"
AWS_S3_CUSTOM_DOMAIN = f"{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com"

# Static and Media settings
MEDIAFILES_LOCATION = "portfolio/media"

# Static and Media URLs
MEDIA_URL = f"https://{AWS_S3_CUSTOM_DOMAIN}/{MEDIAFILES_LOCATION}/"

# Cache control for static files
AWS_S3_OBJECT_PARAMETERS = {
    "CacheControl": "max-age=86400",  # Cache pour 1 jour
}

# File Overwrite
AWS_S3_FILE_OVERWRITE = False  # Ne pas écraser les fichiers existants

# Storage backend configuration
STORAGES = {
    "default": {
        "BACKEND": "portfolio.storages.MediaStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedStaticFilesStorage",
    },
}


# Configuration des domaines de confiance pour les requêtes CSRF
CSRF_TRUSTED_ORIGINS = env("TRUSTED_ORIGINS").split(",")

# Activation des cookies sécurisés (uniquement transmis via HTTPS)
SESSION_COOKIE_SECURE = True
CSRF_COOKIES_SECURE = True

# Paramètres de sécurité HTTPS renforcés
SECURE_HSTS_SECONDS = 31536000  # Active HSTS (HTTP Strict Transport Security) pendant 1 an
SECURE_HSTS_INCLUDE_SUBDOMAINS = True  # Applique HSTS à tous les sous-domaines
SECURE_HSTS_PRELOAD = True  # Indique aux navigateurs de précharger HSTS
SECURE_CONTENT_TYPE_NOSNIFF = True  # Empêche les navigateurs de deviner le type de contenu
SECURE_PROXY_SSL_HEADER = (
    "HTTP_X_FORWARDED_PROTO",
    "https",
)  # Indique que les requêtes passent par un proxy HTTPS

# Configuration des administrateurs de l'application
ADMINS = [
    ("Ibrahima", "ibrahima882001@gmail.com")
]  # Les administrateurs recevront des notifications en cas d'erreurs graves
