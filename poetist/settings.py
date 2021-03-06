"""
Django settings for poetist project.

Generated by 'django-admin startproject' using Django 1.10.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.10/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '*)q8$ci#!6y7m+=v--n*36ns6#qr*vn99nvjidtmhfijl2n-vm'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = [
    "0.0.0.0",
    "192.168.1.36",
    'https://stark-harbor-91981.herokuapp.com/', 
    'stark-harbor-91981.herokuapp.com/',
    'https://www.stark-harbor-91981.herokuapp.com/',
    'www.stark-harbor-91981.herokuapp.com/'
]


# Application definition

INSTALLED_APPS = [
    'accounts',
    'core',
    'dashboard',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'storages',
    'crispy_forms',
    'pagedown',
    'markdown_deux',
    'rest_framework',

]
CRISPY_TEMPLATE_PACK = 'bootstrap3'


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'poetist.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'poetist.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/1.10/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Kolkata'

USE_I18N = True

USE_L10N = True

USE_TZ = True

AWS_STORAGE_BUCKET_NAME = 'poetist-static-files'
AWS_ACCESS_KEY_ID = 'AKIAJVMPUP764CR5RNOQ'
AWS_SECRET_ACCESS_KEY = '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'

# Tell django-storages that when coming up with the URL for an item in S3 storage, keep
# it simple - just use this domain plus the path. (If this isn't set, things get complicated).
# This controls how the `static` template tag from `staticfiles` gets expanded, if you're using it.
# We also use it in the next setting.
AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME

# NOW REPLACING THESE LINES TO USE OUR S3 BUCKET MORE ELEGANTLY.
# NOW WE WILL HAVE /static/ FOLDER FOR STATIC FILES, /media/ FOR OUR MEDIA FILES

# # This is used by the `static` template tag from `static`, if you're using that. Or if anything else
# # refers directly to STATIC_URL. So it's safest to always set it.
# STATIC_URL = "https://%s/" % AWS_S3_CUSTOM_DOMAIN
#
# # Tell the staticfiles app to use S3Boto storage when writing the collected static files (when
# # you run `collectstatic`).
# STATICFILES_STORAGE = 'storages.backends.s3boto.S3BotoStorage'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]

# I JUST ADDED A FILE NAMED cumstom_storages.py IN THE SAME DIRECTORY AS manage.oy
STATICFILES_LOCATION = 'static'
STATICFILES_STORAGE = 'custom_storages.StaticStorage'
STATIC_URL = "https://%s/%s/" % (AWS_S3_CUSTOM_DOMAIN, STATICFILES_LOCATION)

# FROM HERE IS THE SETTINGS FOR MEDIA FILES
MEDIAFILES_LOCATION = 'media'
MEDIA_URL = "https://%s/%s/" % (AWS_S3_CUSTOM_DOMAIN, MEDIAFILES_LOCATION)
DEFAULT_FILE_STORAGE = 'custom_storages.MediaStorage'

# THESE LINES WILL SAY THE EXPIRATION OF THIS DATA HAS NOT YET COME, SO USE THESE TILL IT EXPIRES.
AWS_HEADERS = {  # see http://developer.yahoo.com/performance/rules.html#expires
    'Expires': 'Thu, 31 Dec 2099 20:00:00 GMT',
    'Cache-Control': 'max-age=94608000',
}

# ###################   O L D    S T A T I C    F I L E S 
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/

# Local files
# STATIC_URL = '/static/'

# Copy data from here to server
# STATICFILES_DIRS = [
#     os.path.join(BASE_DIR, "static"),
    #'/var/www/static/',
# ]
# Server emmumator. One up DIR
# STATIC_ROOT = os.path.join(os.path.dirname(BASE_DIR), "static_cdn")

# MEDIA_URL = "/media_cdn/"
# MEDIA_ROOT = os.path.join(os.path.dirname(BASE_DIR), "media_cdn")

