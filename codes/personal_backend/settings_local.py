# coding=UTF-8

SECRET_KEY = "5(15ds+i2+%ik6z&!yer+ga9m=e%jcqiz_5wszg)r-z!2--b2d"

# Postgresql数据库配置
# DATABASES = {
    # 'default': {
        # 'ENGINE': 'django.db.backends.postgresql_psycopg2',
        # 'NAME': 'crm_dev',#'crm_dev',#
        # 'USER': 'bq',
        # 'PASSWORD': 'zxcde321BQ',
        # 'HOST': '192.168.3.250',
        # 'PORT': '5432',
    # },
# }

# MySQL数据库配置
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'best_20180905',
        'USER': 'root',
        'PASSWORD': '',
        'HOST': 'localhost',
        'PORT': 3306
    },
}

# DATABASES = {
    # 'default': {
        # 'ENGINE': 'django.db.backends.postgresql_psycopg2',
        # 'NAME': 'mytest',
        # 'USER': 'postgres',
        # 'PASSWORD': '123918',
        # 'HOST': 'localhost',
        # 'PORT': '5432',
    # },
# }
# Redis配置
REDIS_CONF = {
    'host': 'localhost',
    'port': '6379',
    'max_connections': 100,
}
