# coding=UTF-8

import os

DEBUG = False
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATIC_URL = '/static/'
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "file"),
)

SECRET_KEY = 'n(ga_y0y4l&e8!tyt2)=f5q1=8(b=3&(cwvhfd*w8=0pm(0@00'

# Postgresql
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql_psycopg2',
#         'NAME': 'crm',  # 数据库名字(需要先创建)
#         'USER': 'bq',  # 登录用户名
#         'PASSWORD': 'zxcde321BQ',  # 密码
#         # 'HOST': 'localhost',  # 数据库IP地址,留空默认为localhost
#         'HOST': 'localhost',  # 数据库IP地址,留空默认为localhost
#         'PORT': '5432',  # 端口
#     }
# }

# Mysql数据库配置
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'best',
        'USER': 'root',
        'PASSWORD': '',
        'HOST': 'localhost',
        'PORT': '3306',
    },
}


# MySQL数据库配置
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': 'crm',
#         'USER': 'root',
#         'PASSWORD': 'zxcde321BQ',
#         # 'HOST': 'localhost',
#         'HOST': '192.168.3.250',
#         'PORT': '3306'
#     },
# }


REDIS_CONF = {
    # 'host': 'localhost',
    'host': 'localhost',
    'port': '6379',
    'max_connections': 500 ,
}

FILE_CONF = {
    'host': 'localhost',
    'port': '8001',
    'path': BASE_DIR + '/file/store/',
}

TEST_PORT = "8000"
