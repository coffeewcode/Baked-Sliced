import os
from pathlib import Path
import dotenv
import os
from pythonjsonlogger import jsonlogger

dotenv.load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

SECURE_ACTIVATED = False if os.environ.get("TEST") else True
SESSION_COOKIE_SECURE = SECURE_ACTIVATED
SESSION_COOKIE_HTTPONLY = SECURE_ACTIVATED
SESSION_COOKIE_SAMESITE = SECURE_ACTIVATED

# Application definition
DJANGO_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "drf_yasg",
]

DEPENDENCIES = [
    "rest_framework",
    "django.contrib.gis",
    "geoip2",
]

MY_APPS = [
    "product",
    "additional",
    "order",
    "middleware",
    "delivery",
    "address",
    "shopping_cart",
    "user",
]


INSTALLED_APPS = DJANGO_APPS + DEPENDENCIES + MY_APPS

MIDDLEWARE = [
    "middleware.logging_middleware.RequestLoggingMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "_main.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
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

WSGI_APPLICATION = "_main.wsgi.application"


# Database
if os.environ.get("TEST") == True:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }
    print("\n🎯 Using SQLite for testing purposes.\n")
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": os.environ.get("POSTGRES_DB"),
            "USER": os.environ.get("POSTGRES_USER"),
            "PASSWORD": os.environ.get("POSTGRES_PASSWORD"),
            "HOST": os.environ.get("POSTGRES_HOST", "localhost"),
            "PORT": os.environ.get("POSTGRES_PORT", "5432"),
        }
    }

    print("\n🎯 Connecting to PostgreSQL with the following settings:")
    print(f"  Database : {DATABASES['default']['NAME']}")
    print(f"  User     : {DATABASES['default']['USER']}")
    print(f"  Host     : {DATABASES['default']['HOST']}")
    print(f"  Port     : {DATABASES['default']['PORT']}\n")

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
        "OPTIONS": {
            "min_length": 12,
        },
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.Argon2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher",
]

# Internationalization
LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
STATIC_URL = "static/"

# Default primary key field type
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

#  Logging configuration
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "json": {
            "()": jsonlogger.JsonFormatter,
            "format": """
                %(asctime)s %(levelname)s %(name)s
                %(message)s %(pathname)s %(lineno)d
                %(process)d %(thread)d %(threadName)s
            """,
            "datefmt": "%Y-%m-%dT%H:%M:%SZ",
            "rename_fields": {"levelname": "level", "name": "logger"},
            "json_indent": 4,
            "reserved_attrs": [],
        },
        "verbose": {
            "format": "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)d] %(message)s",
            "datefmt": "%Y-%m-%dT%H:%M:%SZ",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "json" if not DEBUG else "verbose",
        },
        "file": {
            "class": "logging.handlers.TimedRotatingFileHandler",
            "filename": os.path.join(BASE_DIR, "logs/django-app.log"),
            "when": "midnight",
            "backupCount": 30,
            "formatter": "json",
            "encoding": "utf-8",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["console", "file"],
            "level": "INFO",
            "propagate": False,
        },
    },
    "root": {
        "handlers": ["console", "file"],
        "level": "DEBUG" if DEBUG else "INFO",
    },
}

SWAGGER_SETTINGS = {"SECURITY_DEFINITIONS": {"Basic": {"type": "basic"}}}
