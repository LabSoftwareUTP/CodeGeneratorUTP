#encoding:utf-8
"""
Django settings for CodeGenerator project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
try:
    from .local_settings import URL_BASE
except:
    URL_BASE = "http://localhost:8000"
PROJECT_NAME = "CodeGenerator"
PROJECT_DESCRIPTION = "Una plataforma diseñada Generar código rapido y fácil"

LOGIN_URL = "/account/login"
LOGOUT_URL = "/account/logout"
LOGIN_REDIRECT_URL = "/"
FROM_EMAIL = PROJECT_NAME + " <no-reply@daiech.com>"

try:
    from .local_settings import GMAIL_USER, GMAIL_USER_PASS
except:
    pass


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '3rv0q_86ep=z7e%-n@o&agu6g&spgx=931=7upb&h9ha8ht=z6'

# SECURITY WARNING: don't run with debug turned on in production!
try:
    from .local_settings import DEBUG
except:
    DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'apps.inspectdb',
    'apps.website',
    'apps.account',
    'apps.core',
    'captcha',
)

try:
    import django_extensions
    INSTALLED_APPS += INSTALLED_APPS + tuple(['django_extensions'])
except:
    pass

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'CodeGenerator.urls'

WSGI_APPLICATION = 'CodeGenerator.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    },
}
# try:
#     from .temp_databases import TMP_DB
#     DATABASES = DATABASES + TMP_DB
# except:
#     pass
try:
    from .local_settings import MYSQL_USER, MYSQL_PASSWD
except:
    MYSQL_PASSWD = "holamundo"
    MYSQL_USER = "root"

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'es-co'

TIME_ZONE = 'America/Bogota'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/


MEDIA_ROOT = os.sep.join([os.path.dirname(os.path.dirname(__file__)), 'public/media'])
MEDIA_URL = '/media/'

STATIC_URL = '/static/'
STATICFILES_DIRS = (
    os.sep.join([os.path.dirname(os.path.dirname(__file__)), 'public/static']),
)

TEMPLATE_DIRS = (
    os.sep.join([os.path.dirname(os.path.dirname(__file__)), 'templates']),
)


TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.core.context_processors.tz",
    "django.contrib.messages.context_processors.messages",
    'django.core.context_processors.request',
    'apps.website.context_processors.get_project_name',
)