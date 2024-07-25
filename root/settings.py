import os
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv()
SECRET_KEY = os.environ.get("SECRET_KEY")

DEBUG = bool(os.environ.get("DEBUG", default="False").lower() == "true")
ALLOWED_HOSTS = ["*"]

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "apps.apps.AppsConfig",
    'storages',
    'boto3'
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    'whitenoise.middleware.WhiteNoiseMiddleware',
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "root.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "root.wsgi.application"
# ASGI_APPLICATION = 'root.asgi.application'
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [('127.0.0.1', 6379)],
        },
    },
}
# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases
DATABASES = {
    "default": {
        "ENGINE": os.environ.get("DB_ENGINE"),
        "NAME": os.environ.get("DB_NAME"),
        "USER": os.environ.get("DB_USER"),
        "PASSWORD": os.environ.get("DB_PASS"),
        "HOST": os.environ.get("DB_HOST"),
        "PORT": os.environ.get("DB_PORT"),
    }
}

# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

WEBPUSH_SETTINGS = {
    "VAPID_PUBLIC_KEY": "BEkzxGtJJiWIRc616DWPieOxBMULD8A6I3M0xuq1AR3sk6u3UgdwUKl_OEH-55nt6aN6VMZdbSdbAY2XxsaYxGE",
    "VAPID_PRIVATE_KEY": "cCr52OGD7xht8C8e4X297LU1uUrmr2Ac4z__aIQqS1c",
    "VAPID_ADMIN_EMAIL": "baxtiyorovjavlon8@gmail.com"
}
# import logging
#
# LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': False,
#     'handlers': {
#         'console': {
#             'level': 'DEBUG',
#             'class': 'logging.StreamHandler',
#         },
#     },
#     'loggers': {
#         'django': {
#             'handlers': ['console'],
#             'level': 'DEBUG',
#             'propagate': True,
#         },
#     },
# }

# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = "en-us"
AUTH_USER_MODEL = "apps.User"
TIME_ZONE = "Asia/Tashkent"

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/
STATIC_URL = "static/"
STATIC_ROOT = os.path.join(BASE_DIR, "static")  # noqa

MEDIA_URL = "media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")  # noqa

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/login/'

# MinIO settings
MINIO_ENDPOINT = os.environ.get('MINIO_ENDPOINT')
MINIO_ACCESS_KEY = os.environ.get('MINIO_ACCESS_KEY')
MINIO_SECRET_KEY = os.environ.get('MINIO_SECRET_KEY')
MINIO_BUCKET_NAME = os.environ.get('MINIO_BUCKET_NAME')
MINIO_CONSISTENCY_CHECK_ON_START = bool(
    os.environ.get("MINIO_CONSISTENCY_CHECK_ON_START", default="False").lower() == "true")

DEFAULT_FILE_STORAGE = os.environ.get('DEFAULT_FILE_STORAGE')
AWS_S3_ENDPOINT_URL = f'http://{MINIO_ENDPOINT}'
AWS_ACCESS_KEY_ID = MINIO_ACCESS_KEY
AWS_SECRET_ACCESS_KEY = MINIO_SECRET_KEY
AWS_STORAGE_BUCKET_NAME = MINIO_BUCKET_NAME
AWS_S3_FILE_OVERWRITE = bool(
    os.environ.get("AWS_S3_FILE_OVERWRITE", default="False").lower() == "true")
AWS_DEFAULT_ACL = None

# DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"
# AWS_ACCESS_KEY_ID = os.environ.get("MINIO_ACCESS_KEY", "access-key")
# AWS_SECRET_ACCESS_KEY = os.environ.get("MINIO_SECRET_KEY", "secret-key")
# AWS_STORAGE_BUCKET_NAME = os.environ.get("MINIO_BUCKET_NAME", "my-local-bucket")
# AWS_S3_ENDPOINT_URL = os.environ.get('MINIO_ENDPOINT_URL')
# AWS_QUERYSTRING_AUTH = True
# MINIO_CONSISTENCY_CHECK_ON_START = True

# AWS_S3_FILE_OVERWRITE = False
