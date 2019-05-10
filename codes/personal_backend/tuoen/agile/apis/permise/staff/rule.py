# coding=UTF-8

'''
Created on 2016年7月23日

@author: Administrator
'''

from tuoen.sys.core.field.base import CharField, DictField, IntField, ListField, BooleanField
from tuoen.sys.core.api.utils import with_metaclass
from tuoen.sys.core.api.request import RequestField, RequestFieldSet
from tuoen.sys.core.api.response import ResponseField, ResponseFieldSet
from tuoen.sys.core.exception.business_error import BusinessError

from tuoen.agile.apis.base import StaffAuthorizedApi
from tuoen.abs.middleware.rule import rule_register


class List(StaffAuthorizedApi):
    """获取权限列表"""
    request = with_metaclass(RequestFieldSet)

    response = with_metaclass(ResponseFieldSet)
    response.rule_list = ResponseField(ListField, desc = '权限列表', fmt = DictField(desc = "权限", conf = {
        'flag': CharField(desc = "权限标示"),
        'desc': CharField(desc = "权限描述"),
    }))

    @classmethod
    def get_desc(cls):
        return "获取权限列表"

    @classmethod
    def get_author(cls):
        return "Roy"

    def execute(self, request):
        rule_mapping = rule_register.get_rule_mapping()
        return rule_mapping

    def fill(self, response, rule_mapping):
        keys = list(rule_mapping.keys())
        keys.sort()
        data_list = [{
            'flag': rule_mapping[key].all_key,
            'desc': rule_mapping[key].desc,
        } for key in keys]
        response.rule_list = data_list
        return response
