from .base import *

ALLOWED_HOSTS = ['13.124.5.37', 'stocktracker.co.kr']
STATIC_ROOT = BASE_DIR / 'static/'
STATICFILES_DIRS = []
DEBUG = False

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'pybo',
        'USER': 'dbmasteruser',
        'PASSWORD': '05tkfkdgo!',
        'HOST': 'ls-c152d9157d388ff408176e07d31a0d9370be7bb6.cmp3sco2upat.ap-northeast-2.rds.amazonaws.com',
        'PORT': '5432'
    }
}
