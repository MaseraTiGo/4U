# -*- coding: UTF-8 -*-    
# Author: Dongjd
# FileName: helper
# DateTime: 2021/1/4 9:09
# Project: awesome_dong
# Do Not Touch Me!


import datetime
from abc import ABC, abstractmethod

from model.store.model_component import FormComponent

from tuoen.sys.core.exception.business_error import BusinessError


class ComponentParser(ABC):
    TAG = None

    def __init__(self, component):
        self._component = component
        self._tag = int(self._component.get('tag', -1))

    @property
    @abstractmethod
    def parsed_data(self):
        ...


class AgeParser(ComponentParser):
    TAG = [FormComponent.Tag.AGE]

    @property
    def parsed_data(self):
        if self._tag in self.TAG:
            try:
                age = int(self._component.get('value'))
                if age < 0 or age > 999:
                    raise BusinessError('年龄异常!')
            except ValueError:
                return datetime.date(1900, 1, 1)
            return datetime.date.today() - datetime.timedelta(days=age * 365)
        return None


class CommonParser(ComponentParser):
    TAG = [FormComponent.Tag.NAME, FormComponent.Tag.PHONE, FormComponent.Tag.ADDR, FormComponent.Tag.TEXT]
    MAPPING = {FormComponent.Tag.NAME: 32, FormComponent.Tag.PHONE: 16, FormComponent.Tag.ADDR: 128}

    @property
    def parsed_data(self):
        if self._tag in self.TAG:
            value = self._component.get('value', 'unknown')
            if len(str(value)) > self.MAPPING.get(int(self._tag), float('inf')):
                raise BusinessError('数据超长！')
            return value
        return None


class GenderParser(CommonParser):
    TAG = [FormComponent.Tag.GENDER]

    @property
    def parsed_data(self):
        if self._tag in self.TAG:
            try:
                return 'male' if \
                    self._component.get('list')[0].get('label') == '男' else 'female'
            except IndexError as _:
                return 'unknown'
        return None
