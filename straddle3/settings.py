# STRADDLE3.NET

import os
from django.utils.translation import ugettext_lazy as _

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENV_PATH = os.path.abspath( os.path.dirname(__file__) )
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(ENV_PATH, '..', 'static')
PROJECT_STATIC_FOLDER = 'straddle3'
STATICFILES_DIRS = [
    ( PROJECT_STATIC_FOLDER, STATIC_ROOT + '/' + PROJECT_STATIC_FOLDER + '/' ),
]
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(ENV_PATH, '..', 'media')

LOGIN_URL = '/login'
LOGOUT_URL = '/logout'

# Name of site in the document title
DOCUMENT_TITLE = 'straddle3'

# Application definition

CONTRIB_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'leaflet',
    'djgeojson',
    'ckeditor',
    'ckeditor_uploader',
    'imagekit',
]

PROJECT_APPS = [
    'apps.utils',
    'apps.models',
]

INSTALLED_APPS = CONTRIB_APPS + PROJECT_APPS

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'straddle3.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [ 'templates' ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'apps.utils.context_processors.debug_processor',
                'apps.utils.context_processors.site_info_processor',
            ],
        },
    },
]

WSGI_APPLICATION = 'straddle3.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

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


#
# Internationalization
#

LANGUAGE_CODE = 'es'
LANGUAGES = (
    ('es', _('Español')),
    ('ca', _('Catalán')),
    ('en', _('English')),
)

TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ   = True
LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'locale'),
)
DECIMAL_SEPARATOR = '.'


# CKEDITOR

CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'Custom',
        'width'  : '100%',
        'toolbar_Custom': [
            ['Bold', 'Italic', 'Underline'],
            ['NumberedList', 'BulletedList', '-', 'Outdent', 'Indent', '-', 'JustifyLeft', 'JustifyCenter', 'JustifyRight', 'JustifyBlock'],
            ['Link', 'Unlink', 'Image' ],
            ['RemoveFormat', 'Source']
        ]
    },
}

CKEDITOR_UPLOAD_PATH = "uploads/"
CKEDITOR_JQUERY_URL  = "/static/admin/js/vendor/jquery/jquery.min.js"


#
# Import private settings
#
from .private_settings import *
