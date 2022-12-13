# -*- coding: utf-8 -*-
# @File    : helper
# @Project : djangoProject
# @Time    : 2022/12/10 9:47
# once, I want 2 leave my name 2 the history
# sadly, I find that my hair gets pale
"""                     
                                      /             
 __.  , , , _  _   __ ______  _    __/  __ ____  _, 
(_/|_(_(_/_</_/_)_(_)/ / / <_</_  (_/_ (_)/ / <_(_)_
                                                 /| 
                                                |/  
"""

import abc
import json

from frame.utils.redis import RedisBase

SEP = '__'


class GetAction(abc.ABC):
    Action = None
    GetActionMapping = {}

    def __init_subclass__(cls, **kwargs):
        if cls.Action is None:
            raise AttributeError('Action can not be None')
        if not isinstance(cls.Action, str):
            raise TypeError('Action must be instance of str')
        cls.GetActionMapping[cls.Action] = cls

    @classmethod
    @abc.abstractmethod
    def execute(cls, value: str, r_handler: RedisBase):
        raise NotImplementedError

    @classmethod
    def fucking_get_it(cls, key: str, r_handler: RedisBase):
        if SEP in key:
            ans = cls._dispatch(key, r_handler)
        else:
            ans = r_handler.get(key, invert=False)
            if ans is None:
                return ans
            ans = json.loads(ans)
        # if isinstance(ans, dict):
        #     ans = MyDict(ans)
        return ans

    @classmethod
    def _dispatch(cls, key: str, r_handler: RedisBase):
        parts = key.split(SEP)
        if len(parts) != 2:
            raise KeyError(f'{key} has more than one "{SEP}"')
        action, value = parts
        if action not in cls.GetActionMapping:
            raise KeyError(f'action: {action} is not support yet.')
        return cls.GetActionMapping[action].execute(value, r_handler)


class TTL(GetAction):
    Action = 'ttl'

    @classmethod
    def execute(cls, value: str, r_handler: RedisBase):
        return r_handler.ttl(value)


class SetAction(abc.ABC):
    Action = None
    SetActionMapping = {}

    def __init_subclass__(cls, **kwargs):
        if cls.Action is None:
            raise AttributeError('Action can not be None')
        if not isinstance(cls.Action, str):
            raise TypeError('Action must be instance of str')
        cls.SetActionMapping[cls.Action] = cls

    @classmethod
    @abc.abstractmethod
    def execute(cls, key: str, value: str, r_handler: RedisBase):
        raise NotImplementedError

    @classmethod
    def fucking_set_it(cls, key: str, value: any, r_handler: RedisBase):
        if SEP in key:
            cls._dispatch(key, value, r_handler)
        else:
            r_handler.set(key, json.dumps(value))

    @classmethod
    def _dispatch(cls, key: str, value: any, r_handler: RedisBase):
        parts = key.split(SEP)
        if len(parts) != 2:
            raise KeyError(f'{key} has more than one "{SEP}"')
        action, key = parts
        if action not in cls.SetActionMapping:
            raise KeyError(f'action: {action} is not support yet.')
        cls.SetActionMapping[action].execute(key, value, r_handler)


class Keys(SetAction):
    Action = 'keys'

    @classmethod
    def execute(cls, key: str, value: str, r_handler: RedisBase):
        ans = r_handler.keys(value)
        r_handler.set(key, json.dumps(ans))


class Ex(SetAction):
    Action = 'ex'

    @classmethod
    def execute(cls, key: str, value: tuple, r_handler: RedisBase):
        r_handler.set(key, json.dumps(value[0]), ex=int(value[1]))


class IncrBy(SetAction):
    Action = 'incrby'

    @classmethod
    def execute(cls, key: str, value: int, r_handler: RedisBase):
        r_handler.incrby(key, int(value))


class MGet(SetAction):
    Action = 'mget'

    @classmethod
    def execute(cls, key: str, value: list, r_handler: RedisBase):
        ans = r_handler.mget(value)
        ans = [json.loads(item) if item else item for item in ans]
        r_handler.set(key, json.dumps(ans))


class Del(SetAction):
    Action = 'del'

    @classmethod
    def execute(cls, key: str, _: str, r_handler: RedisBase):
        if not _:
            raise ValueError(f'del value can only be True')
        return r_handler.delete(key)


class RCache(object):

    def __init__(self, redis_handler: RedisBase):
        self._redis = redis_handler

    def __getattribute__(self, item: str):
        if item.startswith('_'):
            value = super(RCache, self).__getattribute__(item)
            return value
        return GetAction.fucking_get_it(item, self._redis)

    def __setattr__(self, key: str, value):
        if key.startswith('_'):
            super(RCache, self).__setattr__(key, value)
        else:
            SetAction.fucking_set_it(key, value, self._redis)
