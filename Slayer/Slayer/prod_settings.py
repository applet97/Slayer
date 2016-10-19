"""
Django settings for prod server.
"""
from settings import *

ALLOWED_HOSTS = ['slayer.kz']

#PASSWORD_RESET_LINK = "http://prod.idocs.kz/new_password/{0}/"
#VERIFY_LINK = "http://prod.idocs.kz/register/user/{0}/"

"""
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'slayer',
        'USER': 'slayer_django',
        'PASSWORD': '1590751',
        'HOST': 'localhost',
        'PORT': '',
    }
}
"""

STATIC_ROOT = "static"

DEBUG = False

IS_DEMO = False

SEND_BROKEN_LINK_EMAILS = True

CELERY_SEND_TASK_ERROR_EMAILS = True

#SITE_URL = "https://prod.idocs.kz"

#BROKER_URL = 'redis://redis:6379/0'  # celery backend config.
#CELERY_ACCEPT_CONTENT = ['json']
#CELERY_TASK_SERIALIZER = 'json'
#CELERY_RESULT_SERIALIZER = 'json'