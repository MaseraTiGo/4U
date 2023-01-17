"""
Django settings for djangoProject project.

Generated by 'django-admin startproject' using Django 3.2.16.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""
import os
from pathlib import Path

try:
    import MySQLdb
except ImportError:
    import pymysql

    pymysql.version_info = (1, 4, 13, "final", 0)
    pymysql.install_as_MySQLdb()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-wc$d8()2q!xuvlk-gh-zidyh=o*rm5(j^ah0j*@qp(2eg#psbf'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = [
    'super_dong',
    'wick',
    # 'django.contrib.admin',
    # 'django.contrib.auth',
    # 'django.contrib.contenttypes',
    # 'django.contrib.sessions',
    # 'django.contrib.messages',
    # 'django.contrib.staticfiles',
]

AUTO_MIGRATE_APPS = [
    ('wick', 2, False),
    ('super_dong', 3, True),
]

MIDDLEWARE = [
    # 'django.middleware.security.SecurityMiddleware',
    # 'django.contrib.sessions.middleware.SessionMiddleware',
    # 'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    # 'django.contrib.auth.middleware.AuthenticationMiddleware',
    # 'django.contrib.messages.middleware.MessageMiddleware',
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'djangoProject.urls'

super_dong = os.path.join(BASE_DIR, 'super_dong\\frame\\templates')

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates', BASE_DIR / 'super_dong' / 'templates']
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                # 'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
WSGI_APPLICATION = 'djangoProject.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

# MySQL数据库配置
DATABASES = {
    'default': {

        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'my_shit',
        'USER': 'root',
        'PASSWORD': '123918',
        'HOST': 'localhost',
        'PORT': 3306
    },
}

DATABASE_APPS_MAPPING = {
    "super_dong": "default",
    "wick": "default"
}

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = False

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ======================= superDong ============================================

API_ROUTER_PREFIX = 'apis'

API_REGISTER_FILES = ['super_dong.register_center']


# --------------- clear  mysql -------------------------------


def create_db():
    for hulk in DATABASES.values():
        db = None
        try:
            db = MySQLdb.connect(passwd=hulk["PASSWORD"], user=hulk["USER"])

            c = db.cursor()
            c.execute("""show databases""")
            tables = [item[0] for item in c.fetchall()]
            if hulk["NAME"] not in tables:
                c.execute("""create database %s""" % hulk["NAME"])
                db.commit()
        except Exception as e:
            print(f"{hulk['NAME']} manage mysql db failed: {e}\n")
        finally:
            if db:
                db.close()


create_db()
# --------------- clear  mysql -------------------------------

# ======================= superDong ============================================

STORE_MIGRATIONS_2_DB = True
