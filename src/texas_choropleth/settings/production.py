from .base import *
from .pipeline import *


# Debug Settings
DEBUG = False

TEMPLATE_DEBUG = False

ALLOWED_HOSTS = (
    '.unt.edu',
    'localhost',
)

LOG_DIR = "/var/log/texas-choropleth/"

ASSETS_ROOT = get_secret("ASSETS_ROOT")

# Media Settings
MEDIA_ROOT = os.path.join(ASSETS_ROOT, 'media')

# Staticfile Setttings
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

STATIC_ROOT = os.path.join(ASSETS_ROOT, 'static_final')

# TMP Dir for Choropleth Screenshots
IMAGE_EXPORT_TMP_DIR = os.path.join('/', 'tmp')

# Enable Pipeline
PIPELINE_ENABLED = True

# Database Settings
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': get_secret('DB_NAME'),
        'USER': get_secret('DB_USER'),
        'PASSWORD': get_secret('DB_PASSWORD'),
        'HOST': get_secret('DB_HOST'),
        'PORT': get_secret('DB_PORT')
    }
}

# Email Settings
EMAIL_HOST = get_secret('EMAIL_HOST')

EMAIL_PORT = get_secret('EMAIL_PORT')

EMAIL_HOST_USER = get_secret('EMAIL_HOST_USER')

EMAIL_HOST_PASSWORD = get_secret('EMAIL_HOST_PASSWORD')

EMAIL_USE_TLS = get_secret('EMAIL_USE_TLS')

DEFAULT_FROM_EMAIL = get_secret("DEFAULT_FROM_EMAIL")
