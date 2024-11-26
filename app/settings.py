from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = "django-insecure--9!^hok=c8!&hr23in%zzqxd%s9i@8e23m1ek*jhw65a%z4fj$"

DEBUG = True

ALLOWED_HOSTS = ["tracker.afridev.com.ng"]
# ALLOWED_HOSTS = ["*"]


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "trackers",
    # third party
    "drf_yasg",
    "rest_framework",
    "rest_framework_simplejwt.token_blacklist",
    "corsheaders",
    "rest_framework_simplejwt",
    "django_filters",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    #  # -------CORS-----
    # "django.middleware.common.CommonMiddleware",
    # # -------CORS-----
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "app.urls"

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
            ],
        },
    },
]

WSGI_APPLICATION = "app.wsgi.application"


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.sqlite3",
#         "NAME": BASE_DIR / "db.sqlite3",
#     }
# }


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "cvmstrackerdb",
        "USER": "afriauthdb_owner",
        "PASSWORD": "ZfxjP54cLIdz",
        "HOST": "ep-silent-frost-a2griadk.eu-central-1.aws.neon.tech",
        "PORT": 5432,
        "OPTIONS": {
            "sslmode": "require",
        },
    }
}

# postgresql://afriauthdb_owner:ZfxjP54cLIdz@ep-silent-frost-a2griadk.eu-central-1.aws.neon.tech/cvmstrackerdb?sslmode=require


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "Africa/Lagos"

USE_I18N = True

USE_TZ = True


DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]

MEDIA_URL = "/media/"

MEDIA_ROOT = os.path.join(BASE_DIR, "media")

CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True


CORS_ALLOW_HEADERS = [
    "content-type",
    "x-api-key",
]

CSRF_TRUSTED_ORIGINS = [
    "https://tracker.afridev.com.ng",
]



API_KEY = "rbAZcgfSXQLiHHCzYk8pDU9svNpnoFNZ"