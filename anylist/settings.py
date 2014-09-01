"""
Django settings for anylist project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os


BASE_DIR = os.path.dirname(__file__)


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'j!p49a*j4e+!7&s&cx(&orq=s@u-pd&)i3u#p=$h$@)9-p!qo!'

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'myapp',
    'south',
    'easy_thumbnails',
    'rest_framework',
    'rest_framework.authtoken',
    'rest_framework_swagger',
    'djcelery',
    'compressor',
    'django_jenkins',
)

import djcelery
os.environ["CELERY_LOADER"] = "django"
djcelery.setup_loader()

# AMQP_HOST = 'localhost'
# BROKER_HOST = 'localhost'
# BROKER_PORT = 5672
# BROKER_USER = 'ctulhu'
# BROKER_PASSWORD = 'ShockiNg'
# BROKEN_VHOST = 'myvhost'
BROKEN_URL = 'amqp://ctulhu:ShockiNg@localhost:5672//'
CELERY_ACCEPT_CONTENT = ['json']

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'anylist.urls'

WSGI_APPLICATION = 'anylist.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'product_db',
        'USER': 'ctulhu',
        'PASSWORD': ''
    },
    'slave': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'product_db',
        'USER': 'ctulhu',
        'PASSWORD': '',
        'TEST_MIRROR': 'default'
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'compressor.finders.CompressorFinder',
)

COMPRESS_ENABLED = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

STATIC_URL = '/static/'

DEBUG = True
ALLOWED_HOSTS = ['*']

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)
TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, 'templates'),
)

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

MEDIA_URL = '/media/'

THUMBNAIL_ALIASES = {
    '': {
        'icon': {'size': (75,75), 'crop': True},
        'avatar': {'size': (240, 320), 'crop': True},
    },
}


JENKINS_TASKS = (
    'django_jenkins.tasks.run_pep8',
    'django_jenkins.tasks.run_pyflakes',
    'django_jenkins.tasks.run_csslint',
    'django_jenkins.tasks.with_coverage',
)

PROJECT_APPS = (
    'myapp',
)

SOUTH_MIGRATION_MODULES = {
    'easy_thumbnails': 'easy_thumbnails.south_migrations',
}

# should match SELENIUM_URL_ROOT which defaults to http://127.0.0.1:8000
#LIVE_SERVER_PORT = 8000
DJANGO_LIVE_TEST_SERVER_ADDRESS = 'localhost:8082'


REST_FRAMEWORK = {
    'PAGINATE_BY': 20,
    'PAGINATE_BY_PARAM': 'page_size',
    'MAX_PAGINATE_BY': 100,
    'DEFAULT_MODEL_SERIALIZER_CLASS':
        'rest_framework.serializers.HyperlinkedModelSerializer',

    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ),

    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
    ]
}

CACHEOPS_REDIS = {
    'host': 'localhost',
    'port': 6379,
    'db': 1,
    'socket_timeout': 3
}

# CACHEOPS = {
#     'myapp': (),
#     'myapp.Product': ('filter', 60 * 2)
# }

DDF_DEFAULT_DATA_FIXTURE = 'random'