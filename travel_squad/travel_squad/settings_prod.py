DEBUG = False
ALLOWED_HOSTS = ['*']


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'db1',
        'USER': 'django-ts',
        'PASSWORD': '0765842953',
        'HOST': 'localhost',
        'PORT': '',
    }
}