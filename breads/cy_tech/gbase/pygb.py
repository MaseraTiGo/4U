# -*- coding: utf-8 -*-
# @File    : pygb
# @Project : 4U
# @Time    : 2024/7/29 16:43
# once, I want 2 leave my name 2 the history
# sadly, I find that my hair gets pale
"""                     
                                      /             
 __.  , , , _  _   __ ______  _    __/  __ ____  _, 
(_/|_(_(_/_</_/_)_(_)/ / / <_</_  (_/_ (_)/ / <_(_)_
                                                 /| 
                                                |/  
"""
from pygbase8s import JDBCDriver
from pygbase8s import User
import datetime

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'ng_firewall',
        'USER': 'cyadmin',
        'PASSWORD': 'cykj1235',
        'HOST': 'localhost',
        'PORT': 3306
    },
    'ng_log_data': {
        'NAME': 'ng_log_data',
        'ENGINE': 'django.db.backends.mysql',
        'USER': 'cyadmin',
        'PASSWORD': 'cykj1235',
        'HOST': 'localhost',
        'PORT': 3306,
        # 'OPTIONS': {"init_command": "SET default_storage_engine=MyISAM"}
    },
    'ng_ifw_flow': {
        'NAME': 'ng_ifw_flow',
        'ENGINE': 'django.db.backends.mysql',
        'USER': 'cyadmin',
        'PASSWORD': 'cykj1235',
        'HOST': 'localhost',
        'PORT': 3306,
        # 'OPTIONS': {"init_command": "SET default_storage_engine=MyISAM"}
    }
}

class Server:
    ip = "192.168.203.71"
    port = 9088


server = Server()

driver = JDBCDriver(r'D:\Download\gbasedbtjdbc_3.5.1.jar')
user = User('gbasedbt', '1qaz2wsx#EDC')
conn = driver.connect(server, user, params={'DB_LOCALE': 'zh_CN.utf8',
                                            'CLIENT_LOCALE': 'zh_CN.utf8'})
cursor = conn.cursor()
cursor.execute('drop database if exists db_utf8')
cursor.execute('create database db_utf8 with log')
cursor.execute(
    'create table t1(a int, b varchar(100), c datetime year to second)')

values = [
    (1, 'xiaoming', str(datetime.datetime.now())),
    (2, 'xiaohong', str(datetime.datetime.now())),
    (3, 'xiaolan', str(datetime.datetime.now())),
    (4, 'luyang', str(datetime.datetime.now()))
]
cursor.executemany('insert into t1 values(?, ?, ?)', values)
cursor.execute('select * from t1')
rows = cursor.fetchall()
for row in rows:
    print(row)

cursor.execute("SELECT name FROM sysmaster:sysdatabases;")
rows = cursor.fetchall()
for row in rows:
    print(row)


def create_db_if_not_exist():
    cursor.execute("SELECT name FROM sysmaster:sysdatabases;")
    rs = cursor.fetchall()
    dbs = [i[0].strip() for i in rs]
    for hulk in DATABASES.values():
        db_name = hulk['NAME']
        if db_name not in dbs:
            cursor.execute(f'create database {db_name} with log')

    print(dbs)
    for r in dbs:
        print(r)


if __name__ == '__main__':
    create_db_if_not_exist()
