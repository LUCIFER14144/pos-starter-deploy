import os
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = 'dev-secret-key-change-in-prod'
DEBUG = True
ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'core',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'pos_backend.urls'
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {'context_processors': [
            'django.template.context_processors.debug',
            'django.template.context_processors.request',
            'django.contrib.auth.context_processors.auth',
            'django.contrib.messages.context_processors.messages',
        ]},
    },
]
WSGI_APPLICATION = 'pos_backend.wsgi.application'

DATABASES = {
    'default': {'ENGINE': 'django.db.backends.sqlite3', 'NAME': BASE_DIR / 'db.sqlite3'}
}

AUTH_PASSWORD_VALIDATORS = []
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True
STATIC_URL = '/static/'

# Dev manager PIN (change in production)
MANAGER_PIN = '1234'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ]
}


# --- Production additions ---
import dj_database_url

# Secret & debug via env
SECRET_KEY = os.getenv('SECRET_KEY', SECRET_KEY)
DEBUG = os.getenv('DEBUG', 'False') == 'True'
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '*').split(',') if os.getenv('ALLOWED_HOSTS') else ['*']

# Manager PIN from env (dev default kept earlier)
MANAGER_PIN = os.getenv('MANAGER_PIN', MANAGER_PIN if 'MANAGER_PIN' in globals() else '1234')

# Database (use DATABASE_URL if provided)
DATABASES = {
    'default': dj_database_url.config(default=f"sqlite:///{BASE_DIR / 'db.sqlite3'}")
}

# Static files (WhiteNoise)
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATIC_URL = '/static/'

# Whitenoise middleware (ensure it's in MIDDLEWARE)
if 'whitenoise.middleware.WhiteNoiseMiddleware' not in '\n'.join(MIDDLEWARE):
    MIDDLEWARE.insert(1, 'whitenoise.middleware.WhiteNoiseMiddleware')

# CORS (django-cors-headers)
if 'corsheaders' not in INSTALLED_APPS:
    INSTALLED_APPS.append('corsheaders')
if 'corsheaders.middleware.CorsMiddleware' not in MIDDLEWARE:
    MIDDLEWARE.insert(0, 'corsheaders.middleware.CorsMiddleware')

# CORS configuration
# 1) Allow explicit origins via env var CORS_ALLOWED_ORIGINS
# 2) If not provided, default to allowing common local dev origins
# 3) In DEBUG, allow all origins to simplify local/mobile testing
# 4) You can force allow-all by setting CORS_ALLOW_ALL_ORIGINS=True in env
CORS_ALLOWED_ORIGINS = os.getenv('CORS_ALLOWED_ORIGINS', '')
if CORS_ALLOWED_ORIGINS:
    CORS_ALLOWED_ORIGINS = [u.strip() for u in CORS_ALLOWED_ORIGINS.split(',')]
else:
    CORS_ALLOWED_ORIGINS = [
        'http://localhost:3000',
        'http://localhost:3001',
        'http://127.0.0.1:3000',
        'http://127.0.0.1:3001',
    ]

# Allow-all in DEBUG for easier LAN/mobile access (safe because DEBUG=True only in dev)
if DEBUG:
    CORS_ALLOW_ALL_ORIGINS = True
else:
    # For production or when DEBUG=False, allow forcing allow-all via env (use carefully)
    if os.getenv('CORS_ALLOW_ALL_ORIGINS', '').lower() in ('1','true','yes'):
        CORS_ALLOW_ALL_ORIGINS = True

# Security recommended settings
SECURE_SSL_REDIRECT = os.getenv('SECURE_SSL_REDIRECT', 'False') == 'True'
SESSION_COOKIE_SECURE = os.getenv('SESSION_COOKIE_SECURE', 'False') == 'True'
CSRF_COOKIE_SECURE = os.getenv('CSRF_COOKIE_SECURE', 'False') == 'True'
# --- end production additions ---
