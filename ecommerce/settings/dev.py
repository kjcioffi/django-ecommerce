import sys
import os
from .base import *

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

WORKING_ENV = env("WORKING_ENV", default="ecommerce.settings.dev")

if env("WORKING_ENV", default="ecommerce.settings.dev") != "ecommerce.settings.dev":
    DEBUG = False

DEBUG_TOOLBAR_ENABLED = DEBUG and "test" not in sys.argv

ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=["127.0.0.1", "localhost"])

INTERNAL_IPS = ["127.0.0.1", "localhost"]

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": "db.sqlite3",
    }
}

if DEBUG_TOOLBAR_ENABLED:
    INSTALLED_APPS += ["debug_toolbar"]
    MIDDLEWARE += ["debug_toolbar.middleware.DebugToolbarMiddleware"]

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
DEFAULT_FILE_STORAGE = "django.core.files.storage.FileSystemStorage"

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/
STATIC_URL = "static/"
MEDIA_URL = "media/"
STATIC_ROOT = os.path.join("static")
MEDIA_ROOT = os.path.join("media")