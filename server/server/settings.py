from datetime import timedelta
import os

from configurations import Configuration, values
from pathlib import Path


class Dev(Configuration):

    # Build paths inside the project like this: BASE_DIR / 'subdir'.
    BASE_DIR = Path(__file__).resolve().parent.parent

    DOTENV = os.path.join(BASE_DIR, '.env.dev')

    # Quick-start development settings - unsuitable for production
    # See https://docs.djangoproject.com/en/{{ docs_version }}/howto/deployment/checklist/


    # SECURITY WARNING: keep the secret key used in production secret!
    SECRET_KEY = values.SecretValue()

    # SECURITY WARNING: don't run with debug turned on in production!
    DEBUG = True

    ALLOWED_HOSTS = values.ListValue([], separator=';')

    CSRF_TRUSTED_ORIGINS = values.ListValue([], separator=';')

    # Application definition

    INSTALLED_APPS = [
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        'rest_framework',
        'rest_framework_simplejwt',
        'drf_yasg',
        'corsheaders',
        'flights',
        'celery',
        'django_celery_results',
        'django_celery_beat',
    ]

    MIDDLEWARE = [
        'django.middleware.security.SecurityMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
        "corsheaders.middleware.CorsMiddleware",
        "django.middleware.common.CommonMiddleware",
    ]

    ROOT_URLCONF = 'server.urls'

    TEMPLATES = [
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': [],
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

    WSGI_APPLICATION = 'server.wsgi.application'


    # Password validation
    # https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators
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

    # Database
    # https://docs.djangoproject.com/en/{{ docs_version }}/ref/settings/#databases
    # http://django-configurations.readthedocs.org/en/latest/values/#configurations.values.DatabaseURLValue

    DATABASES = {
        "default": {
            "ENGINE": os.environ.get("SQL_ENGINE"),
            "NAME": os.environ.get("SQL_DATABASE"),
            "USER": os.environ.get("SQL_USER"),
            "PASSWORD": os.environ.get("SQL_PASSWORD"),
            "HOST": os.environ.get("SQL_HOST"),
            "PORT": os.environ.get("SQL_PORT"),
        }
    }


    DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
    # Internationalization
    # https://docs.djangoproject.com/en/{{ docs_version }}/topics/i18n/

    LANGUAGE_CODE = 'es-AR'

    TIME_ZONE = 'America/Buenos_Aires'

    USE_I18N = True

    USE_L10N = True

    USE_TZ = True

    # Static files (CSS, JavaScript, Images)
    # https://docs.djangoproject.com/en/{{ docs_version }}/howto/static-files/

    STATIC_URL = values.Value('/static/')

    # MP_ACCESS_TOKEN = values.SecretValue()

    AUTH_USER_MODEL = 'flights.User'


    REST_FRAMEWORK = {
        'DEFAULT_AUTHENTICATION_CLASSES': [
            'rest_framework_simplejwt.authentication.JWTAuthentication',
        ]


    }

    SIMPLE_JWT = {
        "ACCESS_TOKEN_LIFETIME": timedelta(minutes=5),
        "REFRESH_TOKEN_LIFETIME": timedelta(days=15),
    }



    SWAGGER_SETTINGS = {
        "SECURITY_DEFINITIONS": {
            "token": {
                "type": "apiKey",
                "name": "Authorization",
                "in": "header"
            },
        },
    }

    LOGGING = {
        'version': 1,
        'filters': {
            'require_debug_true': {
                '()': 'django.utils.log.RequireDebugTrue',
            }
        },
        'handlers': {
            'console': {
                'level': 'DEBUG',
                'filters': ['require_debug_true'],
                'class': 'logging.StreamHandler',
            }
        },
        'loggers': {
            # 'django.db.backends': {
            #     'level': 'DEBUG',
            #     'handlers': ['console'],
            # }
        }
    }

    CELERY_RESULT_BACKEND = values.Value()
    CELERY_BROKER_URL = values.Value()


class Prod(Dev):
    """
    The in-production settings.
    """

    DOTENV = os.path.join(Dev.BASE_DIR, '.env.dev')
    DEBUG = False
    TEMPLATE_DEBUG = DEBUG

