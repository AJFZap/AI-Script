"""
Django settings for ai_script_app project.

Generated by 'django-admin startproject' using Django 5.0.3.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

from pathlib import Path
from decouple import config
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['*']

# EMAILING SETTINGS
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = config('E_HOST')
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = config('E_HOST_USER')
EMAIL_HOST_PASSWORD = config('E_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = config('DEF_FROM_EMAIL')

PASSWORD_RESET_TIMEOUT = 14400

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework.authtoken',
    'script_generator',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'ai_script_app.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates'],
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

WSGI_APPLICATION = 'ai_script_app.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': config('DB_HOST'),
    }
}

AUTH_USER_MODEL = 'script_generator.CustomUser'

# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    # {
    #     'NAME': 'django_password_validators.password_character_requirements.password_validation.PasswordCharacterValidator',
    #     'OPTIONS': {
    #          'min_length_digit': 1,
    #          'min_length_upper': 1,
    #      }
    # },
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 8,  # Adjust the minimum length as needed
        }
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
    # {
    #     'NAME': 'django.contrib.auth.password_validation.UppercaseValidator',
    # },
    # {
    #     'NAME': 'django.contrib.auth.password_validation.LowercaseValidator',
    # },
]

AUTH_PASSWORD_VALIDATION_MESSAGES = {
    'too_short': "Password must be at least 8 characters long.",
    'password_entirely_numeric': "Password can't be entirely numeric.",
    'password_common': "Password is too common.",
    'password_at_least_one_digit': "Password must contain at least one digit.",
    'password_at_least_one_letter': "Password must contain at least one letter.",
    'password_at_least_one_uppercase': "Password must contain at least one uppercase letter.",
}


# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = 'templates/'

if DEBUG:
    STATICFILES_DIRS = (
        os.path.join(BASE_DIR, "templates/"),
    )
else:
    STATIC_ROOT = os.path.join(BASE_DIR, "templates/")

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, "media/")

LOGIN_URL = 'login'

