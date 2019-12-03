
from configurations import Configuration

import os


class Base(Configuration):

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    ROOT_PATH = os.path.abspath(os.path.dirname(__name__))

    TEMPLATES_DIR = os.path.join(ROOT_PATH, 'templates')

    FRONTEND_DIR = os.path.join(ROOT_PATH, 'frontend')

    SECRET_KEY = 'hs1jb!@*+#%@z&xmh#_!dv@3l7cjhy@h6xs@0&8v-lozc1m5e+'

    INSTALLED_APPS = [
        'grappelli',
        'django.contrib.admin',
        'django.contrib.auth',
        'django_registration',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',

        'personal_cabinet',
        'products',
        'orders',
        'index',
        'cart',
        'statistic',
        'articles',
        'handbook',

        'corsheaders',
        'rest_framework',
        'webpack_loader',
        'django_cleanup',
        'multi_form_view',
        'pytils',
        'ckeditor',
        'phonenumber_field',
        'django.contrib.sites',
        'django.contrib.flatpages',
        'flatpage',
        'seo',
        'mptt',
        'flatblocks'

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
        'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
        'seo.middleware.url_seo_middleware',
        'corsheaders.middleware.CorsMiddleware',
        'django.middleware.common.CommonMiddleware',
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
                'index.context_processors.menu.menu',
                ],
            'libraries':{

                }
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

    LOGOUT_REDIRECT_URL = 'index:index'

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

    SEO_MODELS = [
        'products.research',
        'articles.article'
    ]   

    MPTT_ADMIN_LEVEL_INDENT = 20

    ACCOUNT_ACTIVATION_DAYS = 14

    REST_FRAMEWORK = {
        # Use Django's standard `django.contrib.auth` permissions,
        # or allow read-only access for unauthenticated users.
        # 'DEFAULT_PERMISSION_CLASSES': [
        #     'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
        # ]
    }

    WEBPACK_LOADER = {
        'DEFAULT': {
            'CACHE': True,
            'BUNDLE_DIR_NAME': 'bundles/',  # must end with slash
            'STATS_FILE': os.path.join(FRONTEND_DIR, 'webpack-stats.json'),
        }
    }

    CORS_ORIGIN_ALLOW_ALL = True



class Dev(Base):

    BASE_DIR = Base.BASE_DIR
    DEBUG = True

    SITE_ID = 2

    ALLOWED_HOSTS = ['*']

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'imex',
            'USER': 'oleg',
            'PASSWORD': '22oleg03',
            'HOST': '127.0.0.1',
            'PORT': '5432'
            }
    }

    INTERNAL_IPS = [

        '127.0.0.1',
    ]

    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
    DEFAULT_FROM_EMAIL = '22golomonzin@gmail.com'

    @property
    def INSTALLED_APPS(self):
        return list(Base.INSTALLED_APPS) + [('debug_toolbar'), ('django_extensions')]

    @property
    def MIDDLEWARE(self):
        return list(Base.MIDDLEWARE) + [('debug_toolbar.middleware.DebugToolbarMiddleware')]


class Prod(Base):
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    EMAIL_HOST = 'smtp.gmail.com'
    EMAIL_USE_TLS = True
    EMAIL_PORT = 587
    EMAIL_HOST_USER = 'imexstats@gmail.com'
    EMAIL_HOST_PASSWORD = 'opmiktrihhpfgaam'

    DEBUG = False
    ALLOWED_HOSTS = ['imex.naminteresno.ru']

    SITE_ID = 7
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

    

