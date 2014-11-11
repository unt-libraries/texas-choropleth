from .base import *


# Debug Settings
DEBUG = False

TEMPLATE_DEBUG = False

# Media Settings
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Staticfile Setttings
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

STATIC_ROOT = os.path.join(BASE_DIR, 'static_final')

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
EMAIL_HOST = ''

EMAIL_PORT = ''

EMAIL_HOST_USER = ''

EMAIL_HOST_PASSWORD = ''

EMAIL_USE_TLS = ''

EMAIL_USE_SSL = ''
