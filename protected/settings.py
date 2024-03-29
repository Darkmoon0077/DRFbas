import os
from pathlib import Path
from datetime import timedelta

BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = 'django-insecure-#1z_xe-ou5%o&-&$f1$y$ya11sx*r!q!j&*#n-r!+#n40*8m_='
DEBUG = True
ALLOWED_HOSTS = ['localhost', '0.0.0.0', '127.0.0.1', '161.35.223.73']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'daphne',
    'django.contrib.staticfiles',
    'rest_framework',
    'authorz',
    'authorz.services',
    'rest_framework_simplejwt',
    'drf_yasg',
    'storages',
    'psycopg2',
    'pytils',
    'PIL',
    'behave_django',
    'channels'
]
ASGI_APPLICATION = 'protected.asgi.application'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'protected.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

WSGI_APPLICATION = 'protected.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': os.environ.get('DB_DRIVER','django.db.backends.postgresql'),
        'USER': os.environ.get('PG_USER','zerg'),
        'PASSWORD':os.environ.get('PG_PASSWORD','zergling'),
        'NAME': os.environ.get('PG_DB','prdb'),
        'PORT': os.environ.get('PG_PORT','5432'),
        'HOST': os.environ.get('PG_HOST','localhost'), # uses the container if set, otherwise it runs locally
    }
}


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
STATIC_URL = 'static/'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
AUTH_USER_MODEL = 'authorz.User'
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=1),
    'SLIDING_TOKEN_LIFETIME': timedelta(days=14),
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=1),
}

SWAGGER_SETTINGS = {
    'SECURITY_DEFINITIONS': {
        'JWT Token': {
            'type': 'apiKey',
            'name': 'Authorization',
            'in': 'header'
        }
    },
}
if DEBUG==True:
    STATIC_URL = '/static/'
    STATIC_ROOT = (BASE_DIR / 'static')
    STATICFILES_DIRS = [BASE_DIR / 'templates/src']
    MEDIA_ROOT = (BASE_DIR / 'media')
    MEDIA_URL = '/media/'
else :
    STATIC_URL = '/static/'
    STATIC_ROOT = (BASE_DIR , 'templates/src/static')
    STATICFILES_DIRS = [(BASE_DIR, 'templates/src')]
    MEDIA_ROOT = (BASE_DIR, 'media')
    MEDIA_URL = '/media/'
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = '587'
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'darkmoon0077@gmail.com'
EMAIL_HOST_PASSWORD = 'nzfj uvpb zehj pkbf'
EMAIL_SERVER = EMAIL_HOST_USER
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
EMAIL_ADMIN = ['darkmoon0077@gmail.com']
LOGIN_REDIRECT_URL = 'authorz:fancy_post'
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [("redis", 6379)],
        },
    },
}