# -*- coding: utf-8 -*-
# @File    : __init__.py
# @Project : djangoProject
# @Time    : 2022/12/10 9:43
# once, I want 2 leave my name 2 the history
# sadly, I find that my hair gets pale
"""                     
                                      /             
 __.  , , , _  _   __ ______  _    __/  __ ____  _, 
(_/|_(_(_/_</_/_)_(_)/ / / <_</_  (_/_ (_)/ / <_(_)_
                                                 /| 
                                                |/  
"""

import redis

try:
    from settings import REDIS_CONF
except ImportError as _:
    REDIS_CONF = {
        'host': 'localhost',
        'port': '6379',
        'max_connections': 100,
    }


class RedisBase(object):

    def __init__(self, db=0, prefix=None, no_prefix=False, delimiter=":"):
        self._prefix = "superDong" if not prefix else prefix
        self._no_prefix = no_prefix
        self._delimiter = delimiter

        pool = redis.ConnectionPool(host=REDIS_CONF['host'],
                                    port=REDIS_CONF['port'],
                                    max_connections=int(
                                        REDIS_CONF['max_connections']), db=db)
        self.helper = redis.Redis(connection_pool=pool)

    def generate_key(self, name):
        if self._no_prefix:
            return name
        return "{}{}{}".format(self._prefix, self._delimiter, name)

    def set(self, name, value, ex=None, px=None, nx=False,
            xx=False):
        name_key = self.generate_key(name)
        return self.helper.set(name_key, value, ex, px, nx, xx)

    def get(self, name, invert=True):
        name_key = self.generate_key(name)
        result = self.helper.get(name_key)
        result = result if result is None else result.decode()
        if invert and result is not None and result.isdigit():
            result = int(result)
        return result

    def delete(self, name):
        name_key = self.generate_key(name)
        return self.helper.delete(name_key)

    def bulk_delete(self, *names):
        return self.helper.delete(*names)

    def hset(self, name, key=None, value=None, mapping=None):
        name = self.generate_key(name)
        return self.helper.hset(name, key=key, value=value, mapping=mapping)

    def hdel(self, name, key=None):
        name = self.generate_key(name)
        return self.helper.hdel(name, key)

    def hget(self, name, key):
        name = self.generate_key(name)
        data = self.helper.hget(name, key)
        return None if data is None else data.decode()

    def hgetall(self, name, invert=True):
        name = self.generate_key(name)
        data = self.helper.hgetall(name)
        if data is None:
            return data
        if not invert:
            return dict(
                [(key.decode(), value.decode()) for key, value in data.items()])
        return dict([(int(
            key.decode()) if key.decode().isdigit() else key.decode(), int(
            value.decode()) if value.decode().isdigit() else value.decode()) for
                     key, value in data.items()])

    def hvals(self, name):
        name = self.generate_key(name)
        return self.helper.hvals(name)

    def ttl(self, name):
        name_key = self.generate_key(name)
        return self.helper.ttl(name_key)

    def mget(self, name_list):
        new_name_list = []
        for key in name_list:
            name_key = self.generate_key(key)
            new_name_list.append(name_key)

        values = self.helper.mget(new_name_list)
        if values:
            return [value.decode("utf-8") for value in values]
        return []

    def expire(self, name, ex=0):
        name_key = self.generate_key(name)
        self.helper.expire(name_key, time=ex)

    def sadd(self, key, value, ):
        name = self.generate_key(key)
        return self.helper.sadd(name, value)

    def smembers(self, key):
        name = self.generate_key(key)
        return self.helper.smembers(name)

    def spop(self, key, count=1):
        name = self.generate_key(key)
        return [int(x) for x in self.helper.spop(name, count)]

    def keys(self, name):
        return self.helper.keys(name)

    def lpush(self, key, values):
        return self.helper.lpush(key, values)

    def rpush(self, key, values):
        self.helper.rpush(key, values)

    def brpop(self, key, timeout):
        return self.helper.brpop(key, timeout)

    def blpop(self, key, timeout):
        return self.helper.blpop(key, timeout)

    def lrange(self, name, start, end):
        return self.helper.lrange(name, start, end)

    def setex(self, name, time, value):
        name_key = self.generate_key(name)
        return self.helper.setex(name_key, time, value)


redis_sys = RedisBase(db=0)
