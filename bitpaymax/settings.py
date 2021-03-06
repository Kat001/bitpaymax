from pathlib import Path
import os
from django.contrib import messages


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-vwud%*8kx)-^8e8-ts70nx#h-8v4m6c^!n0-b-#!!q@z1r10%)'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'tailwind',
    'rest_framework',

    'account',
    'profile_app',
    'home',
    'payment',
    'admin_panel'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'bitpaymax.urls'
AUTH_USER_MODEL = 'account.Account'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'


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

WSGI_APPLICATION = 'bitpaymax.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql_psycopg2',
#         'NAME': 'bitpaymax',
#         'USER': 'postgres',
#         'HOST': 'localhost',
#         'PASSWORD': '2012',
#         'PORT': '5432',
#         }
#     }

import dj_database_url
db_from_env = dj_database_url.config(conn_max_age=600)
DATABASES['default'].update(db_from_env)



# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

STATIC_ROOT = os.path.join(BASE_DIR, 'assets')

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

MESSAGE_TAGS = {
    messages.ERROR: 'danger'
}

COINPAYMENTS_API_KEY = '4b4f7c51d0583384f082cc6894b40149063f17036da52bd7b7965a18fc53e89d'
COINPAYMENTS_API_SECRET = 'b33162fc07f678eaB1d9aab22e5dc739eDb8a5030a0748e58bd7763F604cA4bd'

OPENBANK_API_KEY = '8e504350-31d6-11ec-abe2-15b49c29343f'
OPENBANK_API_SECRET = '5b5e73ed8386cf33e2ddf14d7e6cccccef9b817a'
OPENBANK_AUTH = OPENBANK_API_KEY+':'+OPENBANK_API_SECRET
OPENBANK_BASE_URL = "https://icp-api.bankopen.co"

# Twilio setup varioables....
TWILIO_S_ID = "AC3e216bef2b2d10f3d43b8eb3aa9e7b9e"
TWILIO_AUTH_TOKEN = "959f6756d49879626854eefc142cad87"

MEDIA_ROOT = os.path.join(BASE_DIR, 'static_cdn', 'media_root')

MEDIA_URL = '/media/'

SECURE_SSL_REDIRECT = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
