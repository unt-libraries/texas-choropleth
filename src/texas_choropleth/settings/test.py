from .base import *

DEBUG = True
TEMPLATE_DEBUG = True

INSTALLED_APPS += (
    'model_mommy',
)

STATICFILES_STORAGE = 'pipeline.storage.PipelineStorage'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'choropleth',
    }
}
