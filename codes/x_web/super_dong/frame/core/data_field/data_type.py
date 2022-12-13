# -*- coding: utf-8 -*-
# @File    : response
# @Project : djangoProjectTest001
# @Time    : 2022/9/30 9:27
"""
                                      /
 __.  , , , _  _   __ ______  _    __/  __ ____  _,
(_/|_(_(_/_</_/_)_(_)/ / / <_</_  (_/_ (_)/ / <_(_)_
                                                 /|
                                                |/
"""

__all__ = ('RequestData', 'ResponseData')

from super_dong.frame.core.exception import AttrTypeError, AttrNotSupportError, \
    AttrConflictError
from super_dong.frame.core.http.request import request_access_method


class RData(type):
    _FIELD_PROCESSOR = {}

    def __new__(mcs, *args, **kwargs):
        dante = super(RData, mcs).__new__(mcs, *args, **kwargs)
        _attrs = args[-1]  # type: dict
        dante._superDong = args[0]
        dante._field_attr_mapping = {k: v for k, v in _attrs.items() if not k.startswith('__')}
        for attr, value in _attrs.items():
            cls_name = value.__class__.__name__
            if cls_name in dante._FIELD_PROCESSOR:
                dante._FIELD_PROCESSOR[cls_name](value)
        return dante


class ResponseData(metaclass=RData):
    _FIELD_PROCESSOR = {
        'DateTimeField': lambda x: setattr(x, '_to_str', True),
        'FileField': lambda x: setattr(x, '_to_path', True)
    }


class RequestData(metaclass=RData):
    _FIELD_PROCESSOR = {}

    def as_dict(self):
        return vars(self)


def access_method_processor(access_method: list):
    invalid = [item for item in access_method if not isinstance(item, str)]
    if invalid:
        raise AttrTypeError(
            f'access method must be str. invalid method: {invalid}')

    unsupported = set([item.upper() for item in access_method]) - \
                  set(request_access_method)
    if unsupported:
        raise AttrNotSupportError(
            f'access method: {unsupported} is not supported.')


ex_attrs_mapping = {
    'access_method': access_method_processor
}


def access_control(access_method=None, **ex_kwargs):
    access_method = access_method if access_method is not None else request_access_method
    ex_kwargs["access_method"] = access_method
    invalid_attr = [attr for attr in ex_kwargs if attr not in ex_attrs_mapping]
    if invalid_attr:
        raise AttrNotSupportError(f'attrs: {invalid_attr} are not supported.')

    def wrapper(cls):
        for name, value in ex_kwargs.items():
            ex_attrs_mapping[name](value)
            if name in cls.__dict__:
                raise AttrConflictError(
                    f'{cls.__name__} already has the attr: {name}'
                )
            setattr(cls, name, value)
        return cls

    return wrapper
