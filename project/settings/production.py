from .base import *
import django_heroku

DEBUG = False
ALLOWED_HOSTS = ['yourproject.example.com']
django_heroku.settings(locals())
