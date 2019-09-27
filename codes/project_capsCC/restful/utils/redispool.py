# -*- coding: utf-8 -*-
# file_name       : redispool.py
# file_func       :
# file_author     : 'Johnathan.Wick'
# file_create_date: 2019/9/26 10:19
import redis

pool = redis.ConnectionPool(host='localhost', port=6379, db=1)
