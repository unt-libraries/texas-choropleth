from .base import *
from .pipeline import *


# Debug Settings
DEBUG = True

TEMPLATE_DEBUG = True

STATIC_ROOT = os.path.join(BASE_DIR, 'static_final')

# TMP Dir for Choropleth Screenshots
IMAGE_EXPORT_TMP_DIR = os.path.join('/', 'tmp')

INVITE_SIGNUP_SUCCESS_URL = "/"

INSTALLED_APPS += (
    'debug_toolbar',
)

INTERNAL_IPS = (
    '172.17.42.1',
)

# Database Settings
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'texas_choropleth',
        'USER': 'root',
        'PASSWORD': 'root',
        'HOST': os.environ.get('DB_1_PORT_3306_TCP_ADDR'),
        'PORT': os.environ.get('DB_1_PORT_3306_TCP_PORT'),
    }
}

IMAGE_EXPORT_TMP_DIR = os.path.join('/', 'tmp')

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

PIPELINE_ENABLED = False

# This allows us to "test" the pipeline configuration
# just by flipping the PIPELINE_ENABLED constant above.
if PIPELINE_ENABLED:
    # Let Pipeline find Compressed files
    STATICFILES_FINDERS = (
        'django.contrib.staticfiles.finders.FileSystemFinder',
        'django.contrib.staticfiles.finders.AppDirectoriesFinder',
        'pipeline.finders.PipelineFinder',
    )
