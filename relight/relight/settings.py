from pathlib import Path
from datetime import timedelta
import os
from dotenv import load_dotenv
load_dotenv()  # Loads the environment variables from the .env file



# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

SECRET_KEY = os.getenv('SECRET_KEY').strip('"')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
]


SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=15),  # Lifespan of the access token
    'REFRESH_TOKEN_LIFETIME': timedelta(days=14),    # Lifespan of the refresh token
    'ROTATE_REFRESH_TOKENS': True,                # Whether to rotate refresh tokens
    'BLACKLIST_AFTER_ROTATION': True,              # Blacklist refresh tokens after rotation
    'AUTH_COOKIE': 'access_token',                 # Name of the HttpOnly cookie for the access token
    'AUTH_COOKIE_SECURE': True,                    # Send the cookie over HTTPS only
    'AUTH_COOKIE_HTTP_ONLY': True,                 # Make the cookie inaccessible to JavaScript
    'AUTH_COOKIE_SAMESITE': 'None',                 # Restrict cross-site cookie behavior
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
}


REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
}

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework_simplejwt', 
    'forums',
    'library',
    'cloudinary',
    'cloudinary_storage',
    'rest_framework_simplejwt.token_blacklist',
    'corsheaders',
    'django_rest_passwordreset',
    'accounts.apps.AccountsConfig',
]


CLOUDINARY_STORAGE = {
    'CLOUD_NAME': os.getenv('CLOUD_NAME'),
    'API_KEY': os.getenv('CLOUD_API_KEY'),
    'API_SECRET': os.getenv('CLOUD_API_SECRET'),
}
CLOUDINARY_URL = os.getenv('CLOUDINARY_URL')

# Allow frontend domain for CORS
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173", 
]

SESSION_COOKIE_SAMESITE = 'None'
CSRF_COOKIE_SAMESITE = 'None'
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True


DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'
STATICFILES_STORAGE = 'cloudinary_storage.storage.StaticHashedCloudinaryStorage'

MEDIA_URL = '/media/'


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
]

ROOT_URLCONF = 'relight.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'relight.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'relight_db',  # The name of your PostgreSQL database
        'USER': 'postgres',  # The PostgreSQL user you created
        'PASSWORD': 'binbin',  # The password for your PostgreSQL user
        'HOST': 'localhost',  # For local development
        'PORT': '5432',  # Default PostgreSQL port
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

EMAIL_BACKEND = 'django.core.mail.backends.locmem.EmailBackend'

# EMAIL_BACKEND       = os.getenv('EMAIL_BACKEND')
EMAIL_HOST          = os.getenv('EMAIL_HOST')
EMAIL_PORT          = int(os.getenv('EMAIL_PORT', '0'))
EMAIL_USE_TLS       = os.getenv('EMAIL_USE_TLS') == 'True'
EMAIL_HOST_USER     = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL  = os.getenv('DEFAULT_FROM_EMAIL')