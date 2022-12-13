# -*- coding: utf-8 -*-
# @File    : __init__.py
# @Project : djangoProject
# @Time    : 2022/10/12 9:57
"""
                                      /
 __.  , , , _  _   __ ______  _    __/  __ ____  _,
(_/|_(_(_/_</_/_)_(_)/ / / <_</_  (_/_ (_)/ / <_(_)_
                                                 /|
                                                |/
"""

from abc import ABC, abstractmethod


class InitRepo(object):
    MySons = []

    def __init_subclass__(cls, **kwargs):
        cls.MySons.append(cls)


class BaseError(ABC, Exception):

    @classmethod
    @abstractmethod
    def get_code(cls) -> int:
        pass

    @classmethod
    @abstractmethod
    def get_desc(cls) -> str:
        pass


class RouteError(BaseError, InitRepo, ABC):
    MySons = []


class RouteServiceNotFoundError(RouteError):
    @classmethod
    def get_code(cls) -> int:
        return 50001

    @classmethod
    def get_desc(cls) -> str:
        return 'route service is not founded.'


class DataError(BaseError, InitRepo, ABC):
    MySons = []


class DataKeyMissingError(DataError):
    @classmethod
    def get_code(cls) -> int:
        return 40001

    @classmethod
    def get_desc(cls) -> str:
        return 'data key is missing.'


class DataMemberConflictError(DataError):
    @classmethod
    def get_code(cls) -> int:
        return 40002

    @classmethod
    def get_desc(cls) -> str:
        return 'data member conflict.'


class DataProcessorNotSupportError(DataError):
    @classmethod
    def get_code(cls) -> int:
        return 40003

    @classmethod
    def get_desc(cls) -> str:
        return 'data processor does not support yet.'


class AttrError(BaseError, InitRepo, ABC):
    MySons = []


class AttrMissingError(AttrError):
    @classmethod
    def get_code(cls) -> int:
        return 30001

    @classmethod
    def get_desc(cls) -> str:
        return 'attr missing.'


class AttrConflictError(AttrError):
    @classmethod
    def get_code(cls) -> int:
        return 30002

    @classmethod
    def get_desc(cls) -> str:
        return 'attr conflict.'


class AttrNotSupportError(AttrError):
    @classmethod
    def get_code(cls) -> int:
        return 30003

    @classmethod
    def get_desc(cls) -> str:
        return 'attr does not support yet.'


class AttrTypeError(AttrError):
    @classmethod
    def get_code(cls) -> int:
        return 30004

    @classmethod
    def get_desc(cls) -> str:
        return 'attr type is invalid.'


class ApiError(BaseError, InitRepo, ABC):
    MySons = []


class ApiNotRegisterError(ApiError):
    @classmethod
    def get_code(cls) -> int:
        return 20001

    @classmethod
    def get_desc(cls) -> str:
        return 'the api does not exist or registered.'


class HttpError(BaseError, InitRepo, ABC):
    MySons = []


class HttpCtnTypeConflictError(HttpError):
    @classmethod
    def get_code(cls) -> int:
        return 10000

    @classmethod
    def get_desc(cls) -> str:
        return 'the content type of response is conflict.'


class HttpMethodNotSupportError(HttpError):
    @classmethod
    def get_code(cls) -> int:
        return 10001

    @classmethod
    def get_desc(cls) -> str:
        return 'the method of requesting does not support yet.'


class HttpCtnTypeNotMatchError(HttpError):

    @classmethod
    def get_code(cls) -> int:
        return 10002

    @classmethod
    def get_desc(cls) -> str:
        return 'the content type of request or response ' \
               'does not match the repo\'s'


class BusinessLogicError(BaseError):
    @classmethod
    def get_code(cls) -> int:
        return 44444

    @classmethod
    def get_desc(cls) -> str:
        return 'something wrong with ur codes.'


"""
醉裡挑燈看劍
夢回吹角連營
八百里分麾下炙
五十弦翻塞外聲
沙場秋點兵
馬作的盧飛快
弓如霹靂弦驚
了卻君王天下事
贏得生前身後名
可憐白髮生
"""
