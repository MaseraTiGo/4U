# -*- coding: utf-8 -*-
# @File    : __init__.py
# @Project : djangoProjectTest001
# @Time    : 2022/9/30 11:03
"""
                                      /
 __.  , , , _  _   __ ______  _    __/  __ ____  _,
(_/|_(_(_/_</_/_)_(_)/ / / <_</_  (_/_ (_)/ / <_(_)_
                                                 /|
                                                |/
"""

from abc import ABC
from abc import abstractmethod


class ApiBase(ABC):
    TEST_ATTR = None

    def __call__(self, *args, **kwargs):
        pass

    @abstractmethod
    def __init_subclass__(cls, **kwargs):
        pass

    @classmethod
    @abstractmethod
    def get_desc(cls):
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def get_author(cls):
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def get_history(cls):
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def get_unique_num(cls):
        raise NotImplementedError

    @abstractmethod
    def execute(self):
        raise NotImplementedError

    @abstractmethod
    def tidy(self, *args, **kwargs):
        raise NotImplementedError


class AuthBase(object):
    ...


class NoAuth(AuthBase):
    pass


class Authenticate(AuthBase):
    pass


class Authorize(object):
    ...


class AuthApi(ApiBase, Authenticate, Authorize, ABC):
    ROUTE_MAPPING = {}

    def __init_subclass__(cls, **kwargs):
        # if not hasattr(cls, 'sup_tags'):
        #     raise AttrMissingError('classmethod: sup_tags missing.')
        #
        # tags = []
        # if isinstance(cls.sup_tags(), str):
        #     pass
        pass
