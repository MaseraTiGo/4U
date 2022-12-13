# -*- coding: utf-8 -*-
# @File    : data_field.py
# @Project : djangoProjectTest001
# @Time    : 2022/9/24 9:59
"""                     
                                      /             
 __.  , , , _  _   __ ______  _    __/  __ ____  _, 
(_/|_(_(_/_</_/_)_(_)/ / / <_</_  (_/_ (_)/ / <_(_)_
                                                 /| 
                                                |/  
"""

import abc
import datetime
from typing import Any, List, Iterable

from super_dong.frame.core.exception import DataError


class BaseField(abc.ABC):

    def __init__(self, verbose: str = None, validators: List = None,
                 choices: List = None, is_required: bool = True, default=None,
                 **kwargs):
        if not verbose:
            raise DataError(
                f'{self.__class__.__name__}\'s verbose can not be empty str or None'
            )
        self._verbose = verbose
        self._validators = validators if validators is not None else []
        self._choices = choices if choices is not None else []
        self.is_required = is_required
        self.default = default

    @abc.abstractmethod
    def _parse(self, value) -> Any:
        pass

    def _validator_perform(self, value):
        for validator in self._validators:
            if not validator(value):
                raise DataError(
                    f'value: {value} can not pass {validator.__name__}\' checking.'
                )

    def _choices_check(self, value):
        choices = [item[0] for item in self._choices]
        if choices and value not in choices:
            raise DataError(
                f'{self._name}\'s value: "{value}" is not in choices: {choices}'
            )

    def __set_name__(self, owner, name):
        self._name = name

    def __set__(self, instance, value):
        value = self._parse(value)
        self._validator_perform(value)
        self._choices_check(value)

        instance.__dict__[self._name] = value

    def __get__(self, instance, owner):
        return instance.__dict__[self._name] if instance else None


class BooleanField(BaseField):

    def _parse(self, value) -> Any:
        return True if value else False


class IntField(BaseField):
    def __init__(self, min_value: int = None, max_value: int = None, **kwargs):
        self._min = min_value
        self._max = max_value
        super(IntField, self).__init__(**kwargs)

    def _parse(self, value) -> Any:
        try:
            value = int(value)
        except ValueError as e:
            raise DataError(e)
        else:
            if self._min is not None and value < self._min:
                raise DataError(
                    f'value: {value} is less than {self._min}')
            if self._max is not None and value > self._max:
                raise DataError(
                    f'value: {value} is great than {self._max}')

        return value


class FloatField(IntField):

    def _parse(self, value) -> Any:
        try:
            value = float(value)
        except ValueError as e:
            raise DataError(e)
        else:
            if self._min is not None and value < self._min:
                raise DataError(
                    f'value: {value} is less than {self._min}')
            if self._max is not None and value > self._max:
                raise DataError(
                    f'value: {value} is great than {self._max}')

        return value


class CharField(BaseField):

    def __init__(self, max_length: int = None, **kwargs):
        super(CharField, self).__init__(**kwargs)
        if max_length is None:
            raise ValueError('CharField must have attr: max_length')
        if not isinstance(max_length, int):
            raise ValueError('CharField\'s attr: max_length must be integer.')
        if max_length < -1:
            raise ValueError(
                'max length can not less than -1(-1 means non-limit)')

        self._max_length = max_length

    def _parse(self, value) -> Any:
        if not isinstance(value, (str, int)):
            raise ValueError(f'"{value}" is not a valid char')

        value = str(value)

        if len(value) > self._max_length != -1:
            raise DataError(
                f'the length of "{value}" is greater than {self._max_length}')
        return value


class ListField(BaseField):

    def __init__(self, item: BaseField = None, **kwargs):
        super(ListField, self).__init__(**kwargs)
        if hasattr(item, 'NEST') and not item.NEST:
            raise DataError(
                f'{item.__class__.__name__} can not be nested.')
        self._item = item

    def _parse(self, value) -> Any:
        if not isinstance(value, Iterable):
            raise DataError(
                f'{self._name}\'s value: <{value}> is not iterable.')

        tmp_obj = type('list_tmp_cls', (), {'tmp': self._item})()
        for item in value:
            try:
                tmp_obj.tmp = item
            except ValueError as e:
                raise DataError(e)
        return value


class DictField(BaseField):

    def __init__(self, members: dict, strict: bool = False, **kwargs):
        super(DictField, self).__init__(**kwargs)
        self._strict = strict
        for _, field_cls in members.items():
            if hasattr(field_cls, 'NEST') and not field_cls.NEST:
                raise DataError(
                    f'{field_cls.__class__.__name__} can not be nested.')
        self._members = members

    def _parse(self, value: dict) -> Any:
        if not isinstance(value, dict):
            raise DataError(f'{self._name}\'s value is not a dict')

        if self._strict:
            missing_key = set(self._members.keys()) - set(value.keys())
            if missing_key:
                raise DataError(
                    f'{self._name}\'s keys: \'{", ".join(missing_key)}\' is/are missing.')

        tmp_obj = type('dict_tmp_cls', (), self._members)()

        for key, v in value.items():
            try:
                setattr(tmp_obj, key, v)
            except ValueError as e:
                raise DataError(e)
        return value


class DateTimeField(BaseField):

    def __init__(self, to_str: bool = False, **kwargs):
        self._to_str = to_str
        super(DateTimeField, self).__init__(**kwargs)

    def _parse(self, value) -> Any:
        if isinstance(value, str):
            try:
                value = datetime.datetime.strptime(value, "%Y-%m-%d %H:%M:%S")
            except Exception as _:
                raise DataError(
                    f'{self._name}\'s format must be like: "1992-09-27 00:00:00"')
        elif isinstance(value, datetime.datetime):
            pass
        else:
            raise DataError(
                f'{self._name} must be a str or datetime format, not {type(value)}')
        if self._to_str:
            value = value.strftime("%Y-%m-%d %H:%M:%S")
        return value


class AlmightyField(BaseField):

    def _parse(self, value) -> Any:
        return value


class FileField(CharField):
    NEST = False

    def __init__(self, to_path: bool = False, **kwargs):
        kwargs['max_length'] = 250
        super(FileField, self).__init__(**kwargs)
        self._to_path = to_path

    def _parse(self, value) -> Any:
        if self._to_path and not isinstance(value, str):
            raise DataError(f'response file-field must be a path str')
        return value
