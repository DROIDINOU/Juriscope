from pathlib import Path
import os
#from dotenv import load_dotenv

# Charge uniquement les variables d'environnement locales si le fichier .env existe
#if os.path.exists(".env"):
    #load_dotenv()
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-7yj+gzat15m40er!d#(ci*#@c=rt=$()y0u7tr05c01euoe$l7'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['juriscope.onrender.com', 'localhost', '127.0.0.1', '6297ec3f0568.ngrok-free.app']

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',  # Correcte la ligne ici
    'veille',  # Ajoute cette ligne pour ton application 'veille'
    'corsheaders',  # Ajoute cette ligne pour le CORS
]

SESSION_COOKIE_SAMESITE = "None"
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SAMESITE = "None"
CSRF_COOKIE_SECURE = True

CORS_ALLOWED_ORIGINS = [
    "https://hypothes.is",
    "https://6297ec3f0568.ngrok-free.app",
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Ajoute cette ligne
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'monsite.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

WSGI_APPLICATION = 'monsite.wsgi.application'

# Database configuration for PostgreSQL
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME'),  # Récupère la variable d'environnement DB_NAME
        'USER': os.getenv('DB_USER'),  # Récupère la variable d'environnement DB_USER
        'PASSWORD': os.getenv('DB_PASSWORD'),  # Récupère la variable d'environnement DB_PASSWORD
        'HOST': os.getenv('DB_HOST', 'localhost'),  # Récupère DB_HOST ou 'localhost' si non défini
        'PORT': os.getenv('DB_PORT', '5432'),      # Récupère DB_PORT ou '5432' si non défini
    }
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'

# Répertoire où tu mets tes fichiers statiques durant le développement
STATICFILES_DIRS = [BASE_DIR / 'static']

# Répertoire où Django va collecter les fichiers statiques en production
STATIC_ROOT = BASE_DIR.parent / 'staticfiles'
print("⚠️ STATIC_ROOT =", STATIC_ROOT)
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
