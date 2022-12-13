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
        pass

    @classmethod
    @abstractmethod
    def get_author(cls):
        pass

    @classmethod
    @abstractmethod
    def get_history(cls):
        pass

    @classmethod
    @abstractmethod
    def get_unique_num(cls):
        pass

    @abstractmethod
    def execute(self):
        pass

    @abstractmethod
    def tidy(self, *args, **kwargs):
        pass


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

    @classmethod
    @abstractmethod
    def get_desc(cls):
        pass

    @classmethod
    @abstractmethod
    def get_author(cls):
        pass

    @classmethod
    @abstractmethod
    def get_history(cls):
        pass

    @classmethod
    @abstractmethod
    def get_unique_num(cls):
        pass

    @abstractmethod
    def execute(self):
        pass

    @abstractmethod
    def tidy(self, *ret):
        pass

