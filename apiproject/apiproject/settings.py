"""
Django settings for apiproject project.
"""

from pathlib import Path
from os import environ

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = environ.get("DJANGO_SECRET_KEY")

ALLOWED_HOSTS = ["localhost", "127.0.0.1", "0.0.0.0"]


INSTALLED_APPS = [
    "django.contrib.contenttypes",
    "django_celery_results",
    "rest_framework",
    "apiapp",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "apiproject.urls"

WSGI_APPLICATION = "apiproject.wsgi.application"

REST_FRAMEWORK = {
    "UNAUTHENTICATED_USER": None,
    "EXCEPTION_HANDLER": "apiapp.utils.custom_exception_handler",
    "DEFAULT_RENDERER_CLASSES": [
        "rest_framework.renderers.JSONRenderer",
    ],
    "DEFAULT_PARSER_CLASSES": [
        "rest_framework.parsers.JSONParser",
    ],
}

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": environ.get("POSTGRES_DB"),
        "USER": environ.get("POSTGRES_USER"),
        "PASSWORD": environ.get("POSTGRES_PASSWORD"),
        "HOST": environ.get("POSTGRES_HOST"),
        "PORT": environ.get("POSTGRES_PORT"),
    }
}

CELERY_RESULT_BACKEND = "django-db"
CELERY_BROKER_URL  = f'amqp://{environ.get("RABBITMQ_DEFAULT_USER")}:{environ.get("RABBITMQ_DEFAULT_PASS")}@{environ.get("RABBITMQ_HOST")}:{environ.get("RABBITMQ_PORT")}//'

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
