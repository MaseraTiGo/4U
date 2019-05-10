# coding=UTF-8

'''
Created on 2016年7月26日

@author: Administrator
'''

import redis

from tuoen.settings import REDIS_CONF
from tuoen.utils.common.single import Single

class RedisCache(Single):
    
    def __init__(self):
        pool = redis.ConnectionPool(**REDIS_CONF)
        self.helper = redis.Redis(connection_pool = pool)
    
    def set(self,name,value, ex=None, px=None, nx=False, xx=False):
        return self.helper.set(name, value, ex, px, nx, xx) 
    
    def get(self,name):
        return self.helper.get(name).decode()
    
    def set_map(self,name, mapping):
        return self.helper.hmset(name, mapping) 
    
    def get_map(self,name):
        return self.helper.hgetall(name)
    
    def delete(self,name,*args):
        return self.helper.delete(name,*args)
    
redis_cache = RedisCache()
    
    