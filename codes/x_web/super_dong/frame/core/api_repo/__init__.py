# -*- coding: utf-8 -*-
# @File    : __init__.py
# @Project : djangoProjectTest001
# @Time    : 2022/10/11 10:30
"""
                                      /
 __.  , , , _  _   __ ______  _    __/  __ ____  _,
(_/|_(_(_/_</_/_)_(_)/ / / <_</_  (_/_ (_)/ / <_(_)_
                                                 /|
                                                |/
"""
import abc
import json

from django.conf import settings
from django.core.handlers.wsgi import WSGIRequest

from super_dong.frame.core.exception import HttpCtnTypeConflictError, \
    ApiNotRegisterError, AttrMissingError


def gen_api_name_by_cls(api):
    prefix = settings.API_ROUTER_PREFIX
    api_name = api.__module__ + '.' + api.__name__.lower()  # type: str
    api_name = api_name[api_name.index(prefix) + len(prefix) + 1:]
    api_name = api_name.replace('api.', '')
    return api_name


class CtnManager(object):
    PROCESSOR_MAPPING = {}

    @classmethod
    def register(cls, ctn_type: str, fn: callable) -> None:
        if ctn_type in cls.PROCESSOR_MAPPING:
            raise HttpCtnTypeConflictError(f'{ctn_type} is already exist.')
        cls.PROCESSOR_MAPPING[ctn_type] = fn


def app_json_ctn_processor(request: WSGIRequest) -> dict:
    return {
        key: value
        for key, value in json.loads(request.body.decode("utf-8")).items()
    }


def x_form_ctn_processor(request: WSGIRequest) -> dict:
    return {
        key: value
        for key, value in request.POST.items()
    }


def form_data_process(request: WSGIRequest) -> dict:
    return {
        'File': {'files': request.FILES}

    }


CtnManager.register('application/json', app_json_ctn_processor)
CtnManager.register('application/x-www-form-urlencoded', app_json_ctn_processor)
CtnManager.register('form-data', form_data_process)


class BaseRepo(abc.ABC):
    SERVICE_NAME = None
    SERVICE_TAG = None
    ACCEPT = None
    CONTENT_TYPE = None

    _INDIVIDUAL_API_MAPPING = None
    FULL_API_MAPPING = {}

    def __init_subclass__(cls, **kwargs):
        for attr in [
            cls.SERVICE_NAME, cls.SERVICE_TAG, cls.ACCEPT, cls.CONTENT_TYPE
        ]:
            if attr is None:
                raise AttrMissingError(
                    f'attr: <SERVICE_NAME|SERVICE_TAG|ACCEPT|CONTENT_TYPE> can not be None')

        if cls.SERVICE_TAG not in cls.FULL_API_MAPPING:
            cls.FULL_API_MAPPING[cls.SERVICE_TAG] = cls

    @classmethod
    def add(cls, *apis):
        cls._INDIVIDUAL_API_MAPPING = cls._INDIVIDUAL_API_MAPPING if cls._INDIVIDUAL_API_MAPPING else {}
        cls._INDIVIDUAL_API_MAPPING.update(
            {gen_api_name_by_cls(api): api for api in
             apis}
        )

    @classmethod
    def get_api_cls(cls, api_str: str):
        api_cls = cls._INDIVIDUAL_API_MAPPING.get(api_str)
        if not api_cls:
            raise ApiNotRegisterError(f'api: {api_str} is not implement yet.')
        return api_cls
