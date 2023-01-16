# -*- coding: utf-8 -*-
# @File    : __init__.py
# @Project : djangoProjectTest001
# @Time    : 2022/9/30 11:00
"""
                                      /
 __.  , , , _  _   __ ______  _    __/  __ ____  _,
(_/|_(_(_/_</_/_)_(_)/ / / <_</_  (_/_ (_)/ / <_(_)_
                                                 /|
                                                |/
"""

__all__ = ('SuperDongProtocol', 'initialize_api_repo_files')

import importlib
from typing import Tuple

from django.conf import settings
from django.core.handlers.wsgi import WSGIRequest

from super_dong.apis.admin.account.api import Login
from super_dong.frame.core.api import ApiBase
from super_dong.frame.core.api_repo import BaseRepo, CtnManager
from super_dong.frame.core.data_field.data_type import ResponseData, RequestData
from super_dong.frame.core.exception import DataKeyMissingError, \
    DataProcessorNotSupportError, HttpMethodNotSupportError, \
    HttpCtnTypeNotMatchError, RouteServiceNotFoundError


def initialize_api_repo_files():
    try:
        repo_files = settings.API_REGISTER_FILES
    except AttributeError:
        repo_files = []
    if not repo_files:
        warning = "[no api register file was found.]"
        print(f"\033[33m {warning:*^88} \033[39m")
    for file in repo_files:
        importlib.import_module(file)


def get_service_tag_and_api_str(url: str) -> tuple:
    _, service_tag, *api_str = url.strip('/').split('/')
    api_str = f'{service_tag}.{".".join(api_str)}'
    return service_tag, api_str


def get_api_relative_things(request: WSGIRequest) -> Tuple[ApiBase, dict, str]:
    service_tag, api_str = get_service_tag_and_api_str(request.path_info)
    api_repo = BaseRepo.FULL_API_MAPPING.get(service_tag)  # type: BaseRepo
    if not api_repo:
        raise RouteServiceNotFoundError(
            f"service: <{service_tag}> is not exist.")
    if request.content_type != api_repo.ACCEPT:
        raise HttpCtnTypeNotMatchError(f'api requires: {api_repo.ACCEPT}, '
                                       f'but get: {request.content_type}')

    api_cls = api_repo.get_api_cls(api_str)

    data_processor = CtnManager.PROCESSOR_MAPPING.get(api_repo.ACCEPT)
    if not data_processor:
        raise DataProcessorNotSupportError(
            f'header-accept: {api_repo.ACCEPT} is not supported yet.')

    data = data_processor(request)
    return api_cls, data, api_repo.CONTENT_TYPE


class SuperDongProtocol(object):
    initialize_api_repo_files()

    @classmethod
    def _parse_data(cls, api_cls: [ApiBase], data: dict,
                    data_type: [ResponseData, RequestData], api_ins=None,
                    method: str = 'POST'
                    ):
        # -------------------- initialize api_ins ------------------------------

        api_ins = api_cls() if api_ins is None else api_ins  # type: api_cls
        api_cls = api_cls if api_ins is None else api_ins.__class__
        attrs = []
        for attr, deposit_cls in vars(api_cls).items():
            if not hasattr(deposit_cls, '_superDong'):
                continue
            if hasattr(deposit_cls, 'access_method') and \
                    method not in deposit_cls.access_method:
                continue
            if issubclass(deposit_cls, data_type):
                attrs.append(attr)
                setattr(api_ins, attr, deposit_cls())

        # -------------------- initialize api_ins ------------------------------

        # -------------------- attrs & data check ------------------------------

        if not attrs and data:
            raise DataKeyMissingError(
                f"{data_type.__name__} not defined: [Method: {method}]."
            )
        # todo<dong>: execute may not return anything. ---20230113 17:32:00
        if attrs and data is None:
            raise DataKeyMissingError(f"request/tidied data can not be None.")

        # -------------------- attrs & data check ------------------------------

        for attr in attrs:
            if attr not in data:
                raise DataKeyMissingError(
                    f'{data_type.__name__}: "{attr}" is missing.')

            r_ins = getattr(api_ins, attr)
            r_data = data[attr]
            cls._verify_and_process_data(r_ins, r_data, attr)

        return api_ins

    @classmethod
    def _verify_and_process_data(cls, r_ins: [ResponseData, RequestData],
                                 r_data: dict, attr: str):
        for field_name, attr_obj in r_ins._field_mapping_attr.items():
            if field_name in r_data:
                setattr(r_ins, field_name, r_data[field_name])
                r_data[field_name] = getattr(r_ins, field_name)
            else:
                if attr_obj.is_required:
                    raise DataKeyMissingError(
                        f'key: "{field_name}" in data:[{attr}] is required.'
                    )
                if attr_obj.default is not None:
                    r_data[field_name] = attr_obj.default
                    setattr(r_ins, field_name, attr_obj.default)

    @classmethod
    def _gen_api_ins(cls, api_cls: [ApiBase], req_data: dict):
        api_ins = cls._parse_data(api_cls, req_data, RequestData)
        return api_ins

    @classmethod
    def _format_response_data(cls, api_ins: [ApiBase], rsp_data: dict):
        cls._parse_data(None, rsp_data, ResponseData, api_ins=api_ins)

    @classmethod
    def dispatcher(cls, request: WSGIRequest):
        ...

    @classmethod
    def process_request(cls, request: WSGIRequest):
        api_cls, request_data, ctn_type = get_api_relative_things(request)
        if hasattr(api_cls, 'access_method') and \
                request.method not in api_cls.access_method:
            raise HttpMethodNotSupportError(
                f'api: {api_cls.__name__} does not support: {request.method}'
            )
        api_ins = cls._gen_api_ins(api_cls, request_data)
        api_ins.meta_request = request

        ret_data = api_ins.execute()
        if ret_data is not None:
            ret_data = ret_data if isinstance(ret_data, tuple) else (ret_data,)
            tidied_data = api_ins.tidy(*ret_data)
        else:
            tidied_data = {}

        cls._format_response_data(
            api_ins,
            tidied_data
        )
        return tidied_data, ctn_type


if __name__ == '__main__':
    test_data = {
        'Login': {
            'name': "apple",
            'age': 10,
            'hobbits': (1, 2, 3),
            'crypto': {
                'name': 'apple apple',
                'ai': [4, 5, 6]
            },
            'mix': {
                'fuck': [{'you': 'y'}, {'you': 'o'}, {'you': 'u'}, ]
            },

        },
        'InfoDante': {
            'goods': ['banana', 'carrot'],
            'sale_date': '1992-09-27 00:00:00'
        },
        'Almighty': {
            'almighty': [{'name': [1, 2, 3]}]
        },
        'Result': {
            'objects': 'math',
            'score': 99
        }
    }

    ins = SuperDongProtocol._parse_data(Login, test_data, RequestData)

    print(vars(ins.Login))
