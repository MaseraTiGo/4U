# coding=UTF-8

'''
Created on 2016年7月22日

@author: Administrator
'''

import hashlib
import datetime
import json
import time
import random

from tuoen.utils.exception.business_error import BusinessError

class Token(object):
    
    _key_fmt = "{user_id}:token"
    _token_fmt = "{user_id}{timestamp}{random_num}"
    _unique_key = "unique_key"

    def __init__(self,user,auth_token=None, \
                 renewal_flag=None, expire_time = None):
        self.user = user
        self.auth_token = auth_token
        self.renewal_flag = renewal_flag
        self.expire_time = expire_time
        self.check()
        
    @property
    def is_expire(self):
        cur_time = int(time.time())
        return cur_time > self.expire_time
    
    def reset(self, renewal_flag):
        if renewal_flag == self.renewal_flag:
            self._kill()
            self.generate_auth_token()
            return self
        return None
    
    def check(self):
        if any( obj is None for obj in \
                [self.auth_token,self.renewal_flag,self.expire_time]):
            self.generate_auth_token()
        return self
     
    def _get_time_scope(self, hour = 3):
        cur_time = int(time.time())
        expire_time = cur_time + hour * 60 * 60
        return cur_time, expire_time
    
    def get_unique_key(self):
        return self._key_fmt.format(user_id = self.user.id)
    
    def _apply(self):
        if not hasattr(self.__class__, "_token_mapping"):
            self.__class__._token_mapping = {}

        self.__class__._token_mapping[self.auth_token] = json.dumps({
                                            "renewal_flag" : self.renewal_flag,
                                            'user_id':self.user.id,
                                            "expire_time" : self.expire_time,
                                            self._unique_key : self.get_unique_key()
                                        })
        self.__class__._token_mapping[self.get_unique_key()] = self.auth_token
        
    def _kill(self):
        redis_cache.delete(self.get_unique_key())
        redis_cache.delete(self.auth_token)
        
    def generate_auth_token(self):
        cur_time, expire_time = self._get_time_scope()
        random_num = random.randint(1, 99999)
        token_str = self._token_fmt.format(user_id = self.user.id,\
                           timestamp = cur_time,random_num = random_num)
        token_md5 = hashlib.md5(token_str.encode("utf-8")).hexdigest()
        size = int(len(token_md5) / 2)
        self.auth_token = token_md5[:size]
        self.renewal_flag = token_md5[size:]
        self.expire_time = expire_time
        self._apply()
        return self
    
    def json(self):
        return {
            "renewal_flag":self.renewal_flag,
            "auth_token":self.auth_token,
            "expire_time":self.expire_time,
        }
    
    @classmethod
    def _load_token(cls,token_str):
        if not hasattr(self.__class__, "_token_mapping"):
            self.__class__._token_mapping = {}

        auth_token = json.loads(cls._token_mapping.get(token_str))
        unique_key = auth_token.pop(cls._unique_key)
        auth_auth_token = redis_cache.get(unique_key)
        if token_str != auth_auth_token:
            return {}
        return auth_token
    
    @classmethod
    def get_token(cls,token_str):
        try:
            token_info = cls._load_token(token_str)
            token_info.update({"auth_token":token_str})
            user_id = int(token_info.pop('user_id'))
            user = User.get_byid(id = user_id)
            return cls(user,**token_info)
        except:
            return None

