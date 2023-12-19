from main.settings.base import *

SECRET_KEY = "secret"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": "database_test",
        "USER": "root",
        "PASSWORD": "1234_password",
        "HOST": "postgres",
        "PORT": 5432,
    }
}

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.dummy.DummyCache",
    }
}

