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

from super_dong.frame.core.data_field import BaseField
from super_dong.frame.core.exception import AttrTypeError, AttrNotSupportError, \
    AttrConflictError
from super_dong.frame.core.http.request import request_access_method


@classmethod
def display(cls, level=0):
    pivot_index = '    ' * level
    title = f"{pivot_index}@{cls.__name__} - Dict[object] # {cls.__doc__}\n"
    fields = [attr for attr in vars(cls).values() if
              isinstance(attr, BaseField)]
    details = "\n".join([field.display(level=level+1) for field in fields])
    return title + "%s{\n%s\n%s}" % (pivot_index, details, pivot_index)


def _add_processor_4_rdata(field_obj, r_data_cls):
    cls_name = field_obj.__class__.__name__
    if cls_name in r_data_cls._FIELD_PROCESSOR:
        r_data_cls._FIELD_PROCESSOR[cls_name](field_obj)
    elif cls_name == 'ListField':
        _add_processor_4_rdata(field_obj._item, r_data_cls)
    elif cls_name == 'DictField':
        for inner_field_obj in field_obj._members.values():
            _add_processor_4_rdata(inner_field_obj, r_data_cls)


class RData(type):
    _FIELD_PROCESSOR = {}

    def __new__(mcs, *args, **kwargs):
        dante = super(RData, mcs).__new__(mcs, *args, **kwargs)
        _attrs = args[-1]  # type: dict
        dante._superDong = args[0]
        dante.display = display
        dante._field_mapping_attr = {k: v for k, v in _attrs.items() if not k.startswith('__')}
        for field_obj in _attrs.values():
            _add_processor_4_rdata(field_obj, dante)
        return dante


class ResponseData(metaclass=RData):
    _FIELD_PROCESSOR = {
        'DateTimeField': lambda x: setattr(x, '_to_str', True),
        'FileField': lambda x: setattr(x, '_to_path', True)
    }


class RequestData(metaclass=RData):
    _FIELD_PROCESSOR = {}

    @property
    def as_dict(self) -> dict:
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
