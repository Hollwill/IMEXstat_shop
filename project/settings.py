
from configurations import Configuration

import os

class Base(Configuration):

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    ROOT_PATH = os.path.abspath(os.path.dirname(__name__))

    SECRET_KEY = 'hs1jb!@*+#%@z&xmh#_!dv@3l7cjhy@h6xs@0&8v-lozc1m5e+'


    INSTALLED_APPS = [
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        'django_cleanup',
        'multi_form_view',
        'pytils',
        'personal_cabinet',
        'products',
        'orders',
        'index',
        'cart',
        'ckeditor',
        'phonenumber_field',
    ]

    MIDDLEWARE = [
        'django.middleware.security.SecurityMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
        'whitenoise.middleware.WhiteNoiseMiddleware',
    ]

    ROOT_URLCONF = 'project.urls'

    TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(ROOT_PATH, "templates")],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                ],
            },
        },
    ]

    WSGI_APPLICATION = 'project.wsgi.application'

    AUTH_PASSWORD_VALIDATORS = [
        {
            'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
        },
        {
            'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        },
        {
            'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
        },
        {
            'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
        },
    ]

    LANGUAGE_CODE = 'ru-ru'

    TIME_ZONE = 'UTC'

    USE_I18N = True

    USE_L10N = True

    USE_TZ = True

    LOGIN_REDIRECT_URL = 'lk:settings'

    LOGOUT_REDIRECT_URL = 'research:list'

    STATIC_ROOT = os.path.join(ROOT_PATH, 'static')
    STATIC_URL = '/static/'
    STATICFILES_DIRS = (
        os.path.join(ROOT_PATH, 'files',  "static"),
    )
    STATICFILES_FINDERS = (
        'django.contrib.staticfiles.finders.FileSystemFinder',
        'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    )
    MEDIA_ROOT = os.path.join(ROOT_PATH, 'files', 'media')
    MEDIA_URL = '/files/media/'

    ADMIN_MEDIA_PREFIX = '/static/admin/'


    CKEDITOR_BASEPATH = "/static/ckeditor/ckeditor/"



class Dev(Base):

    BASE_DIR = Base.BASE_DIR
    DEBUG = True

    ALLOWED_HOSTS = [ ]

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
            }
    }

    INTERNAL_IPS = [

        '127.0.0.1',
    ]
    @property
    def INSTALLED_APPS(self):
        return list(Base.INSTALLED_APPS) + [('debug_toolbar'), ('django_extensions')]

    @property
    def MIDDLEWARE(self):
        return list(Base.MIDDLEWARE) + [('debug_toolbar.middleware.DebugToolbarMiddleware')]


class Prod(Base):
    DEBUG = False
    ALLOWED_HOSTS = ['imex.naminteresno.ru']

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'imex',
            'USER': 'ubuntu',
            'PASSWORD': 'jmfMbcbm47',
            'HOST': '127.0.0.1',
            'PORT': '5432',
        }
    }

    LOGGING = {
       'version': 1,
       'disable_existing_loggers': False,
       'handlers': {
           'file': {
               'level': 'DEBUG',
               'class': 'logging.FileHandler',
               'filename': '/home/ubuntu/test/IMEXstat_shop/project/debug.log',
           },
           'mail_admins': {
               'level': 'ERROR',
               'class': 'django.utils.log.AdminEmailHandler',
           },       
       },
       'loggers': {
           'django': {
               'handlers': ['file'],
               'level': 'DEBUG',
               'propagate': True,
           },
           'django.request': {
               'handlers': ['mail_admins'],
               'level': 'ERROR',
               'propagate': True,
           },              
       },
    }




    

