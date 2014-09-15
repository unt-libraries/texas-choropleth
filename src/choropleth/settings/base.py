"""
Django settings for choropleth project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

# Project Directory Definitions
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

PROJECT_ROOT = os.path.dirname(BASE_DIR)

LOG_DIR = os.path.join(PROJECT_ROOT, 'log')


SECRET_KEY = 'jw)fm_v6fb8-oh(1o_^23+#0e)d#udtgc%*@$j2038r!!lo($a'

DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []

LOGIN_URL = '/login/'

LOGIN_REDIRECT_URL = '/choropleths/'


# Application definition
DJANGO_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
)

THIRD_PARTY_APPS = (
    'south',
    'pipeline',
    'rest_framework',
)

LOCAL_APPS = (
    'datasets',
    'cartograms',
    'choropleths',
)

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'choropleth.urls'

WSGI_APPLICATION = 'choropleth.wsgi.application'

# Database Settings
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


# Internationalization
LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

DATE_FORMAT = 'N j, Y'


# Template Settings
from django.conf.global_settings import TEMPLATE_CONTEXT_PROCESSORS
TEMPLATE_CONTEXT_PROCESSORS += (
    'django.core.context_processors.request',
)

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, 'templates'),
)


# Media Settings
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

MEDIA_URL = '/media/'

IMAGE_EXPORT_TMP_DIR = os.path.join('/', 'tmp')


# Static Files Settings
STATICFILES_STORAGE = 'pipeline.storage.PipelineCachedStorage'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

STATIC_ROOT = os.path.join(BASE_DIR, 'static_final')

STATIC_URL = '/static/'


# Pipeline Settings
PIPELINE_COMPILERS = (
    'pipeline.compilers.less.LessCompiler',
)

PIPELINE_CSS = {
    'main': {
        'source_filenames': (
            'css/main.less',
        ),
        'output_filename': 'css/main.css',
    }
}

PIPELINE_JS = {
    'map': {
        'source_filenames': (
            'js/colorbrewer.js',
            'js/map.js',
        ),
        'output_filename': 'js/map.js',
    },
    'app': {
        'source_filenames': (
            'js/app.js',
        ),
        'output_filename': 'js/app.js',
    },
    'map-vendor': {
        'source_filenames': (
            'vendor/d3/d3.min.js',
            'vendor/topojson/topojson.js',
            'vendor/showdown/src/showdown.js'
        ),
        'output_filename': 'js/map-vendor.js',
    },
    'vendor': {
        'source_filenames': (
            'vendor/angular/angular.min.js',
            'vendor/angular-resource/angular-resource.min.js',
            'vendor/jquery/dist/jquery.min.js',
            'vendor/bootstrap/dist/js/bootstrap.min.js',
        ),
        'output_filename': 'js/vendor.js',
    }

}
