from .base import *

DEBUG = True
TEMPLATE_DEBUG = True

THIRD_PARTY_APPS += (
    'debug_toolbar',
)

INTERNAL_IPS = (
    # Docker Gateway
    '172.17.42.1',        
)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'choropleth',
        'USER': 'root',
        'PASSWORD': 'root',
        'HOST': os.environ.get('DB_1_PORT_3306_TCP_ADDR'),
        'PORT': os.environ.get('DB_1_PORT_3306_TCP_PORT'),
    }
}

IMAGE_EXPORT_TMP_DIR = os.path.join('/', 'tmp')

