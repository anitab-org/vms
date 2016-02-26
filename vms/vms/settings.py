"""
Django settings for vms project.

Note: Currently development settings. Not suitable as is for production.
"""
from django.core.urlresolvers import reverse_lazy


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'rs473)3n^fe0^t-^s$n)_%pl=75f_na7z5ee@(^xc-vn^bzr%a'

# SECURITY WARNING: run with debug turned off (DEBUG = False) in production!
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
    'administrator',
    'authentication',
    'event',
    'home',
    'job',
    'organization',
    'registration',
    'shift',
    'vms',
    'volunteer',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'vms.urls'

WSGI_APPLICATION = 'vms.wsgi.application'


# Database
# Change these database settings if your database engine, database name,
# username or password changes
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'vms',
        'USER': 'vmsadmin',
        'PASSWORD': '0xdeadbeef',
        'HOST': 'localhost',
    }
}

# Internationalization
LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# Specifies the directory where static files (CSS, JavasScript) are stored
STATIC_URL = '/static/'

# All uploaded files (such as resumes) are stored in the /srv directory
# /srv directory contains site-specific data which is served by the system
MEDIA_ROOT = '/srv/'

# Uploaded files have read and write permissions to the owner only
FILE_UPLOAD_PERMISSIONS = 0o600

FILE_UPLOAD_DIRECTORY_PERMISSIONS = 0o600

# If user fails to authenticate, then they are redirected to the view
# specified in the reverse_lazy call
LOGIN_URL = reverse_lazy('auth:user_login')
