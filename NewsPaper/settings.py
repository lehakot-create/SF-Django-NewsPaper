"""
Django settings for NewsPaper project.

Generated by 'django-admin startproject' using Django 4.0.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""

from pathlib import Path
import os
import django_heroku
import dj_database_url
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-klv(t=hdmqthc1=0y%21v!n2fo@8n7yc%aw&z_)+*4b(o)#ruw'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'modeltranslation',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    # 'whitenoise.runserver_nostatic',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'accounts',
    'news',
    'django_filters',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'django_apscheduler',
    'rest_framework',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    # 'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'news.middlewares.TimezoneMiddleware',
]

ROOT_URLCONF = 'NewsPaper.urls'

LOCALE_PATHS = [
    os.path.join(BASE_DIR, 'locale')
]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
            'libraries': {
                'custom_filters': 'news.templatetags.custom_filters'
            }
        },
    },
]

WSGI_APPLICATION = 'NewsPaper.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/

# LANGUAGE_CODE = 'en-us'
LANGUAGE_CODE = 'ru'

LANGUAGES = [
    ('en-us', 'English'),
    ('ru', 'Русский')
]

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = False



# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

# STATIC_URL = 'static/'
# STATIC_ROOT = BASE_DIR / 'staticfiles'
# STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'


# # STATIC_URL = '/static/'
# STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
# STATICFILES_DIRS = [STATIC_ROOT]
#
#
# STATIC_URL = '/static/'

# STATIC_ROOT = os.path.join(BASE_DIR, "static")
# STATICFILES_DIRS = (os.path.join(BASE_DIR, "staticfiles"),)


# STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTHENTICATION_BACKENDS = [
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',

    # `allauth` specific authentication methods, such as login by e-mail
    'allauth.account.auth_backends.AuthenticationBackend',
]

SITE_ID = 1



ACCOUNT_FORMS = {'signup': 'news.forms.BaseRegisterForm'}
# ACCOUNT_SIGNUP_FORM_CLASS = 'news.forms.SignupForm'

EMAIL_HOST = 'smtp.yandex.ru'
EMAIL_PORT = 465
EMAIL_HOST_USER = 'alex85aleshka@yandex.ru'
EMAIL_HOST_PASSWORD = 'fktirf85fktirf'
EMAIL_USE_SSL = True
DEFAULT_FROM_EMAIL = 'alex85aleshka@yandex.ru'


if DEBUG:
    EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

LOGIN_REDIRECT_URL = '/'
LOGIN_URL = '/accounts/login/'


ACCOUNT_EMAIL_VERIFICATION = 'mandatory'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_AUTHENTIFICATION_METHOD = 'email'
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_USERNAME_REQUIRED = False
# ACCOUNT_EMAIL_VERIFICATION = 'none'
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

# APSCHEDULER_DATETIME_FORMAT = "N j, Y, f:s a"
# APSCHEDULER_RUN_NOW_TIMEOUT = 25  # Seconds

CELERY_IMPORTS = ("news.tasks", )
CELERY_BROKER_URL = 'redis://:vESrrZycyOfUuGFPslEqFmQjdgClZSwb@redis-18169.c277.us-east-1-3.ec2.cloud.redislabs.com:18169/0'
CELERY_RESULT_BACKEND = 'redis://:vESrrZycyOfUuGFPslEqFmQjdgClZSwb@redis-18169.c277.us-east-1-3.ec2.cloud.redislabs.com:18169/0'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'

CELERY_TIMEZONE = "UTC"

# celery -A NewsPaper worker --loglevel=INFO --concurrency 1 -P solo  # а потом вот это
# celery -A NewsPaper worker -l INFO

# celery -A NewsPaper worker -l INFO -B

# celery -A NewsPaper beat    # запускаем сначала это

# celery -A NewsPaper worker -l INFO --loglevel=DEBUG

# celery -A NewsPaper flower  --address=127.0.0.6 --port=5566


db_from_env = dj_database_url.config()
DATABASES['default'].update(db_from_env)

django_heroku.settings(locals())


CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': os.path.join(BASE_DIR, 'Cache_files'),
    }
}



# LOGGING = {
#     'version': 1,
#     'disable_existing_logger': False,
#     'loggers': {
#         'django': {
#             'handlers': ['console', 'console_warning', 'console_err_crit', 'general'],
#             'level': 'DEBUG',
#             'propagate': True,
#         },
#         'django.request': {
#             'handlers': ['errorlog', 'mail_admins'],
#             'level': 'CRITICAL',
#             'propagate': False,
#         },
#         'django.server': {
#             'handlers': ['errorlog', 'mail_admins'],
#             'level': 'CRITICAL',
#             'propagate': False,
#         },
#         'django.template': {
#             'handlers': ['errorlog'],
#             'level': 'ERROR',
#         },
#         'django.db_backends': {
#             'handlers': ['errorlog'],
#             'level': 'ERROR',
#         },
#         'django.security': {
#             'handlers': ['securitylog'],
#             'level': 'ERROR',
#         },
#     },
#     'handlers': {
#         'console': {
#             'level': 'DEBUG',
#             'class': 'logging.StreamHandler',
#             'formatter': 'console',
#             'filters': ['require_debug_true'],
#         },
#         'console_warning': {
#             'level': 'WARNING',
#             'class': 'logging.StreamHandler',
#             'formatter': 'console_warning',
#             'filters': ['require_debug_true'],
#         },
#         'console_err_crit': {
#             'level': 'ERROR',
#             'class': 'logging.StreamHandler',
#             'formatter': 'err_crit',
#             'filters': ['require_debug_true'],
#         },
#         'general': {
#             'level': 'INFO',
#             'class': 'logging.FileHandler',
#             'filename': 'general.log',
#             'formatter': 'general',
#             'filters': ['require_debug_false'],
#         },
#         'errorlog': {
#             'level': 'ERROR',
#             'class': 'logging.FileHandler',
#             'filename': 'error.log',
#             'formatter': 'err_crit',
#         },
#         'securitylog': {
#             'level': 'ERROR',
#             'class': 'logging.FileHandler',
#             'filename': 'security.log',
#             'formatter': 'general',
#         },
#         'mail_admins': {
#             'level': 'ERROR',
#             'class': 'django.utils.log.AdminEmailHandler',
#             'filters': ['require_debug_false'],
#         },
#     },
#     'formatters': {
#         'console': {
#             'format': '{asctime} {levelname} {message}',
#             'datetime': '%Y.%m.%d %H:%M:%S',
#             'style': '{',
#         },
#         'console_warning': {
#             'format': '{asctime} {levelname} {message} {pathname}',
#             'datetime': '%Y.%m.%d %H:%M:%S',
#             'style': '{',
#         },
#         'err_crit': {
#             'format': '{asctime} {levelname} {message} {pathname} {exc_info}',
#             'datetime': '%Y.%m.%d %H:%M:%S',
#             'style': '{',
#         },
#         'general': {
#             'format': '{asctime} {levelname} {module} {message}',
#             'datetime': '%Y.%m.%d %H:%M:%S',
#             'style': '{',
#         }
#     },
#     'filters': {
#         'require_debug_false': {
#             '()': 'django.utils.log.RequireDebugFalse',
#         },
#         'require_debug_true': {
#             '()': 'django.utils.log.RequireDebugTrue',
#         }
#     }
# }


REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 10
}
