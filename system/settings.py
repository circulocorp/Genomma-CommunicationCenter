import os, environ, sys
from pathlib import Path


env: environ.Env = environ.Env(
    DEBUG=(bool, False)
)

BASE_DIR = Path(__file__).resolve().parent.parent

# Switch .env files based on the environment

ENVIRONMENT: str = os.environ.get('ENVIRONMENT', default='development')

print(f'-> Loading {ENVIRONMENT} environment')

if ENVIRONMENT == 'development':
    env.read_env(os.path.join(BASE_DIR, '.env.dev'))
    print('-> Development environment loaded')
elif ENVIRONMENT == 'production':
    env.read_env(os.path.join(BASE_DIR, '.env.prod'))
    print('-> Production environment loaded')
else:
    print('-> Missing ENVIRONMENT variable, set to development or production')
    sys.exit(1)

# Basic configuration

SECRET_KEY = env('DJANGO_SECRET_KEY', cast=str)

DEBUG = env('DJANGO_DEBUG', cast=bool)

ALLOWED_HOSTS = env('DJANGO_ALLOWED_HOSTS', cast=list)

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Third-party apps
    'rest_framework',
    # Local apps
    'core.freight.apps.FreightConfig',
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

ROOT_URLCONF = 'system.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'system.wsgi.application'

# Database

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': env('DATABASE_NAME', cast=str),
        'USER': env('DATABASE_USER', cast=str),
        'PASSWORD': env('DATABASE_PASSWORD', cast=str),
        'HOST': env('DATABASE_HOST', cast=str),
        'PORT': env('DATABASE_PORT', cast=str),
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

# Internationalization

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'America/Mexico_City'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)

STATIC_URL = 'static/'

# Default primary key field type

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Rest Framework

REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    )
}

# RabbitMQ

RABBIT_MQ_HOST = env('RABBIT_MQ_HOST', cast=str)

RABBIT_MQ_DEFAULT_QUEUE = env('RABBIT_MQ_DEFAULT_QUEUE', cast=str)

RABBIT_MQ_USERNAME = env('RABBIT_MQ_USERNAME', cast=str)

RABBIT_MQ_PASSWORD = env('RABBIT_MQ_PASSWORD', cast=str)
