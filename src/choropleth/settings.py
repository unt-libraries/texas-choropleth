"""
Django settings for choropleth project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'jw)fm_v6fb8-oh(1o_^23+#0e)d#udtgc%*@$j2038r!!lo($a'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []

LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/datasets/'

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


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

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
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

DATE_FORMAT = 'N j, Y'

# Cartogram and Cartogram Entity information  will
# be defined in fixtures

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, 'templates'),
)

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
# MEDIA_URL = '/media/'

STATICFILES_STORAGE = 'pipeline.storage.PipelineCachedStorage'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

STATIC_ROOT = os.path.join(BASE_DIR, 'static_final')


STATIC_URL = '/static/'

PIPELINE_COMPILERS = (
    'pipeline.compilers.sass.SASSCompiler',
)

PIPELINE_CSS = {
    'main': {
        'source_filenames': (
            'css/main.scss',
        ),
        'output_filename': 'css/main.css',
    },        
    'colorbrewer': {
        'source_filenames': (
            'css/colorbrewer.css',
        ),
        'output_filename': 'css/colorbrewer.css',
    }
}

PIPELINE_JS = {
    'map': {
        'source_filenames': (
            'js/map.js',
        ),
        'output_filename': 'js/map.js',
    },
    'map-vendor': {
        'source_filenames': (
            'vendor/queue-async/queue.min.js',
            'vendor/d3/d3.min.js',
            'vendor/topojson/topojson.js',
            'vendor/angularjs/angular.min.js',
        ),
        'output_filename': 'js/map-vendor.js',
    },
    'vendor': {
        'source_filenames': (
            'vendor/jquery/dist/jquery.min.js',
            'vendor/bootstrap-sass-official/assets/javascripts/bootstrap.js',
        ),
        'output_filename': 'js/vendor.js',
    }

}
