# -*- coding: utf-8 -*-
# @File    : redis_op
# @Project : hitler_adolf
# @Time    : 2022/6/9 14:25
"""                     
                                      /             
 __.  , , , _  _   __ ______  _    __/  __ ____  _, 
(_/|_(_(_/_</_/_)_(_)/ / / <_</_  (_/_ (_)/ / <_(_)_
                                                 /| 
                                                |/  
"""

import json

import redis

from settings import REDIS_CONF


class RedisBase(object):

    def __init__(self, db=None):
        pool = redis.ConnectionPool(
            host=REDIS_CONF['host'],
            port=REDIS_CONF['port'],
            max_connections=REDIS_CONF['max_connections'],
            db=db or REDIS_CONF['db'],
            password=REDIS_CONF['password']
        )
        self.helper = redis.Redis(connection_pool=pool)

    def set(self, key, value, jsonify=True, ex=None, px=None, nx=False,
            xx=False):
        if jsonify:
            value = json.dumps(value)
        return self.helper.set(key, value, ex, px, nx, xx)

    def get(self, name, invert=True):
        result = self.helper.get(name)
        result = result if result is None else result.decode()
        if invert and result is not None and result.isdigit():
            result = int(result)
        return result

    def keys(self, name):
        values = self.helper.keys(name)
        return [value.decode("utf-8") for value in values]

    def mget(self, name_list, jsonify=True):

        values = self.helper.mget(name_list)

        if values:
            values = [value.decode("utf-8") for value in values]
            if jsonify:
                values = [json.loads(value) for value in values]
        return values


redis_trans_broker = RedisBase()
