# -*- coding: utf-8 -*-
# @File    : gb_injection
# @Project : 4U
# @Time    : 2024/7/30 10:14
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


class Server:
    def __init__(self, ip="127.0.0.1", port=9088):
        self.ip = ip
        self.port = port


class GBClient:

    def __init__(self, user: User, server: Server, jdbc_driver: str, **params):
        self.user = user
        self.server = server
        self.params = params
        default_params = {
            'DB_LOCALE': 'zh_CN.utf8',
            'CLIENT_LOCALE': 'zh_CN.utf8'
        }
        self.params.update(default_params)
        self.jdbc_driver = JDBCDriver(jdbc_driver)

    def __enter__(self):
        self.conn = self.jdbc_driver.connect(self.server, self.user,
                                             params=self.params)
        self.cursor = self.conn.cursor()
        return self.cursor

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cursor.close()
        self.conn.close()
