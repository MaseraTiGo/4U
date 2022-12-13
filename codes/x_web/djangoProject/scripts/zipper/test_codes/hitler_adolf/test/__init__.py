# -*- coding: utf-8 -*-
# @File    : __init__.py
# @Project : hitler_adolf
# @Time    : 2022/6/9 11:48
"""                     
                                      /             
 __.  , , , _  _   __ ______  _    __/  __ ____  _, 
(_/|_(_(_/_</_/_)_(_)/ / / <_</_  (_/_ (_)/ / <_(_)_
                                                 /| 
                                                |/  
"""


import redis

from settings import REDIS_CONF


class RedisBase(object):

    def __init__(self, db=0, prefix=None):
        self._default_prefix = "system" if not prefix else prefix
        pool = redis.ConnectionPool(host=REDIS_CONF['host'],
                                    port=REDIS_CONF['port'],
                                    max_connections=int(
                                        REDIS_CONF['max_connections']), db=db)
        self.helper = redis.Redis(connection_pool=pool)

    def generate_key(self, name, category):
        category = category if category is not None else self._default_prefix
        return "{}:{}".format(category, name)

    def set(self, name, value, category=None, ex=None, px=None, nx=False,
            xx=False):
        name_key = self.generate_key(name, category)
        return self.helper.set(name_key, value, ex, px, nx, xx)

    def get(self, name, category=None, invert=True):
        name_key = self.generate_key(name, category)
        result = self.helper.get(name_key)
        result = result if result is None else result.decode()
        if invert and result is not None and result.isdigit():
            result = int(result)
        return result

    def delete(self, name, category=None):
        name_key = self.generate_key(name, category)
        return self.helper.delete(name_key)

    def bulk_delete(self, *names):
        return self.helper.delete(*names)

    def hset(self, name, key=None, value=None, mapping=None, category=None):
        name = self.generate_key(name, category)
        return self.helper.hset(name, key=key, value=value, mapping=mapping)

    def hget(self, name, key, category=None):
        name = self.generate_key(name, category)
        data = self.helper.hget(name, key)
        return None if data is None else data.decode()

    def hgetall(self, name, invert=True, category=None):
        name = self.generate_key(name, category)
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

    def ttl(self, name, category=None):
        name_key = self.generate_key(name, category)
        return self.helper.ttl(name_key)

    def mget(self, name_list, category=None, prefix=True):
        new_name_list = []
        if prefix:
            for key in name_list:
                name_key = self.generate_key(key, category)
                new_name_list.append(name_key)
        else:
            new_name_list = name_list

        values = self.helper.mget(new_name_list)
        if values:
            return [value.decode("utf-8") for value in values]
        return []

    def expire(self, name, ex=0, category=None):
        name_key = self.generate_key(name, category)
        self.helper.expire(name_key, time=ex)

    def sadd(self, category, key, value, ):
        name = self.generate_key(key, category)
        return self.helper.sadd(name, value)

    def smembers(self, category, key):
        name = self.generate_key(key, category)
        return self.helper.smembers(name)

    def spop(self, category, key, count=1):
        name = self.generate_key(key, category)
        return [int(x) for x in self.helper.spop(name, count)]

    def keys(self, name):
        return self.helper.keys(name)

    def persist(self, key, category=None):
        name = self.generate_key(key, category)
        return self.helper.persist(name)

    def incr(self, key, category=None):
        name = self.generate_key(key, category)
        return self.helper.incr(name)

    def incrby(self, key, amount=0, category=None):
        name = self.generate_key(key, category)
        return self.helper.incrby(name, amount=amount)


redis_sys = RedisBase(db=0)
redis_yaml_settings = RedisBase(db=1)
redis_os_settings = RedisBase(db=2, prefix='openstack')

REPO_THREE_PREFIX = 'ouch'
redis_status_settings = RedisBase(db=3, prefix=REPO_THREE_PREFIX)
redis_instance_info_settings = RedisBase(db=4, prefix='openstack_instance')

REPO_FIVE_PREFIX = 'broker'
redis_trans_broker = RedisBase(db=5, prefix=REPO_FIVE_PREFIX)
