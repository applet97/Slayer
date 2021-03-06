from settings import *


ALLOWED_HOSTS = ["slayer.kz", "18.194.178.77"]

BROKER_URL = 'amqp://mlm:mlm@rabbit:5672/mlm'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'

MEDIA_ROOT = "/media"

STATIC_ROOT = "/static"

SITE_URL = "slayer.kz"

ADMINS_LIST = ['kenenalmat@gmail.com']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'slayer',
        'USER': 'slayeruser',
        'PASSWORD': 'q2HwDqqPZLQt',
        'HOST': 'postgres',
        'PORT': '5432',
    }
}
