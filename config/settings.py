from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent


SECRET_KEY = 'django-insecure-l9(x6x)(2(ej7isd(yitbvkvj%hfm-bz4$dggc31^#+zijlzl)'

DEBUG = True

ALLOWED_HOSTS = ["*"]



INSTALLED_APPS = [
    'unfold',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'rest_framework',
    'rest_framework.authtoken',
    # 'corsheaders',

    'users',
    'courses',

]

MIDDLEWARE = [
    "django.middleware.locale.LocaleMiddleware",
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    # 'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / "templates"],
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

WSGI_APPLICATION = 'config.wsgi.application'


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

AUTH_PASSWORD_VALIDATORS = [
]


LANGUAGE_CODE = 'uz-uz'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

# STATIC_URL = 'static/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Additional

AUTH_USER_MODEL = "users.User"

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.TokenAuthentication",
    ],
}

STATIC_URL = 'static/'
STATIC_ROOT = "static"

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# CORS_ALLOW_ALL_ORIGINS = True
# CORS_ALLOW_CREDENTIALS = True
# CSRF_TRUSTED_ORIGINS = ["https://oztech.uz", "http://localhost:8000"]

LANGUAGE_CODE = "uz"

USE_I18N = True

LANGUAGES = (
    ("uz", "Uzbek"),
    ("en", "English"),
)

UNFOLD = {
    "SHOW_LANGUAGES": True,
}

LOCALE_PATHS = (os.path.join(BASE_DIR, "locale"),)
