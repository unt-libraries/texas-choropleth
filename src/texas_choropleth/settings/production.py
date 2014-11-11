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
        'NAME': '',
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    }
}

# Email Settings
EMAIL_HOST = ''

EMAIL_PORT = ''

EMAIL_HOST_USER = ''

EMAIL_HOST_PASSWORD = ''

EMAIL_USE_TLS = ''

EMAIL_USE_SSL = ''
