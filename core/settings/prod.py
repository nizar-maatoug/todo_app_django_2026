# prod.py

from .base import *

DEBUG = False

ALLOWED_HOSTS = [
    "mydomain.com",
]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "mydb",
        "USER": "myuser",
        "PASSWORD": "secret",
        "HOST": "localhost",
        "PORT": "5432",
    }
}
