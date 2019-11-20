import os

import environ
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

env = environ.Env()
environ.Env.read_env(os.path.join(BASE_DIR, ".env"))

SECRET_KEY = env("SECRET_KEY")

DEBUG = env("DEBUG", bool, False)

ALLOWED_HOSTS = env("ALLOWED_HOSTS", list, ["127.0.0.1", "localhost"])

DATABASES = {"default": env.db()}

EMAIL_CONFIG = env.email_url("EMAIL_URL", default="memorymail://")
vars().update(EMAIL_CONFIG)

HUEY = {"connection": {"url": env("REDIS_URL", default=None)}}


INSTALLED_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "drf_yasg",
    "rules.apps.AutodiscoverRulesConfig",
    "huey.contrib.djhuey",
    "eventos2.core",
    "eventos2.images",
]

# Habilitar a interface de administração apenas em modo debug.
if DEBUG:
    INSTALLED_APPS.append("django.contrib.admin")

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "eventos2.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ]
        },
    }
]

WSGI_APPLICATION = "eventos2.wsgi.application"


# Authentication
# https://docs.djangoproject.com/en/2.2/ref/settings/#authentication-backends

AUTHENTICATION_BACKENDS = (
    "rules.permissions.ObjectPermissionBackend",
    "django.contrib.auth.backends.ModelBackend",
)


# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# Custom user model
# https://docs.djangoproject.com/en/2.2/topics/auth/customizing/

AUTH_USER_MODEL = "core.User"


# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = "pt-br"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = "/api/static/"

STATIC_ROOT = os.path.join(BASE_DIR, "static/")

MEDIA_URL = "/api/media/"

MEDIA_ROOT = os.path.join(BASE_DIR, "media/")

FILE_UPLOAD_PERMISSIONS = 0o640


# Django Rest Framework
# https://www.django-rest-framework.org/
REST_FRAMEWORK = {"DEFAULT_METADATA_CLASS": "eventos2.utils.metadata.MinimalMetadata"}

# Sentry error reporting
# https://docs.sentry.io/platforms/python/django/

SENTRY_URL = env.url("SENTRY_URL", default=None)
if SENTRY_URL:
    sentry_sdk.init(dsn=SENTRY_URL.geturl(), integrations=[DjangoIntegration()])
