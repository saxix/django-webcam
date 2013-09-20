from .settings import *

db = os.environ.get('DBENGINE', None)
if db == 'pg':
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'webcam',
            'HOST': '127.0.0.1',
            'PORT': '',
            'USER': 'postgres',
            'PASSWORD': ''}}
elif db == 'mysql':
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'webcam',
            'HOST': '127.0.0.1',
            'PORT': '',
            'USER': 'root',
            'PASSWORD': ''}}
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': 'webcam.sqlite',
            'HOST': '',
            'PORT': ''}}
