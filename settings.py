"""
Django settings for app project.

Generated by 'django-admin startproject' using Django 1.8.18.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR+"/packages")
sys.path.append(BASE_DIR+"/packages/django")

sys.path.append(os.getcwd()+"/packages")
sys.path.append(os.getcwd()+"/packages/django")
from django.conf.urls import url, include

import quicky


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'bw(lu4t*o&*ot4&gf^&74ksjz3r+ji6bxr_9$y0sacg*ks0m0w'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1', 'localhost','172.16.11.127']
# Application definition

INSTALLED_APPS = (
    'permission_backend_nonrel',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
)
AUTHENTICATION_BACKENDS = [
    'permission_backend_nonrel.backends.NonrelPermissionBackend'
]
MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    # 'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # 'django.middleware.security.SecurityMiddleware',
)



TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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
SESSION_EXPIRE_AT_BROWSER_CLOSE=True
WSGI_APPLICATION = 'wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases
DATABASES = {
   'default' : {
       'ENGINE': 'django_mongodb_engine',
       'NAME': 'lv01_lms',
       'HOST': '172.16.7.63',
       'PORT': 27017,
       'USER': 'sys',
       'PASSWORD': '123456'
   }
}
DATABASES_ = {
   'default' : {
       'ENGINE': 'django_mongodb_engine',
       'NAME': 'hrm',
       'HOST': 'localhost',
       'PORT': 27017,
       'USER': 'root',
       'PASSWORD': '123456'
   }
}


# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = False

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_URL = '/static/'
APPS=[dict(host="default",
           name="argo",
           path="apps/app_main"),
      dict(host="admin",
           name="admin",
           path="apps/admin"),
      dict(host="hrm",
           name="hrm",
           path="apps/hrm"),
      dict(
          host="performance",
          name="performance",
          path="apps/performance"
      )]
aut_config_local_=dict(
    provider="authorization.auth",
    name="hrm",
    host="localhost",
    port=27017,
    user="root",
    password="123456"
)
aut_config_local=dict(
    provider="authorization.auth",
    name="lv01_lms",
    host="172.16.7.63",
    port=27017,
    user="sys",
    password="123456"
)
quicky.authorize.set_config(aut_config_local)

language_congig_local=dict(
    provider="language_mongo_engine",
    name="lv01_lms",
    host="172.16.7.63",
    port=27017,
    user="sys",
    password="123456",
    collection="sys_languages"
)
language_congig_local_=dict(
    provider="language_mongo_engine",
    name="hrm",
    host="localhost",
    port=27017,
    user="root",
    password="123456",
    collection="sys_languages"
)
quicky.language.set_config(language_congig_local)
# argo.language.load(language_congig_local)
# quicky.url.build_urls("apps",APPS)
AUTHORIZATION_ENGINE=quicky.authorize

LANGUAGE_ENGINE=quicky.language
LANGUAGE_CODE="en-us"

ROOT_URLCONF = 'apps'
quicky.url.build_urls(ROOT_URLCONF,APPS)
import os
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': os.getcwd()+os.sep+ 'logs'+os.sep+'debug.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': False,
        },
    },
}
import static_configs



static_configs_db=dict(
    host="172.16.7.63",
    port=27017,
    user="sys",
    password="123456",
    name="lv01_lms",
    collection="sys_settings"
)
static_configs.set_config(static_configs_db)
static_configs.set_data(
    Performance_Settings=dict(
        DateTimeFormat=dict(
            Short_Date_Format="dd/MM/yyyy",
            Date_Format_With_Time="dd/MM/yyyy hh:mm:dd",
            Long_Date_Format="dd MMM yyyy"
        ),
        NumericFormat=dict(
            Group_Seperator=",",
            Decimal_Seperator="."
        )
    ),
    Lms_Settings=dict(

    )

)
STATIC_ROOT = os.path.join(*(BASE_DIR.split(os.path.sep) + ['apps/static','apps/app_main/static']))