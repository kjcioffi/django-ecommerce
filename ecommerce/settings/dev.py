import sys
from .base import (
    env,
    BASE_DIR,
    INSTALLED_APPS,
    MIDDLEWARE,
)

from .base import *

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
WORKING_ENV = env('WORKING_ENV', default="ecommerce.settings.dev")

DEBUG = True

if env('WORKING_ENV', default="ecommerce.settings.dev") != "ecommerce.settings.dev":
    DEBUG = False

DEBUG_TOOLBAR_ENABLED = DEBUG and "test" not in sys.argv

ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=["127.0.0.1", "localhost"])

INTERNAL_IPS = ["127.0.0.1", "localhost"]

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

if DEBUG_TOOLBAR_ENABLED:
    INSTALLED_APPS += ['debug_toolbar']
    MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware']

STATICFILES_STORAGE="whitenoise.storage.CompressedManifestStaticFilesStorage"
DEFAULT_FILE_STORAGE="django.core.files.storage.FileSystemStorage"
