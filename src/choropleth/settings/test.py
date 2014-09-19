from .base import *

DEBUG = False
TEMPLATE_DEBUG = False

INSTALLED_APPS += (
    'model_mommy',
)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'choropleth',
    }
}
