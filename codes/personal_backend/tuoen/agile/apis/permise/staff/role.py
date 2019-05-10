# coding=UTF-8

'''
Created on 2016年7月23日

@author: Administrator
'''

from tuoen.sys.core.field.base import CharField, DictField, IntField, ListField, BooleanField, DatetimeField
from tuoen.sys.core.api.utils import with_metaclass
from tuoen.sys.core.api.request import RequestField, RequestFieldSet
from tuoen.sys.core.api.response import ResponseField, ResponseFieldSet
from tuoen.sys.core.exception.business_error import BusinessError

from tuoen.agile.apis.base import StaffAuthorizedApi
from tuoen.abs.middleware.role import role_middleware
from tuoen.abs.service.permise.manager import RoleServer


class Add(StaffAuthorizedApi):
    """添加角色"""
    request = with_metaclass(RequestFieldSet)
    request.role_info = RequestField(DictField, desc = "角色详情", conf = {
        'name': CharField(desc = "角色名称"),
        'parent_id': IntField(desc = "上级角色id"),
        'rules': CharField(desc = "角色权限", is_required = False),
        'describe': CharField(desc = "角色描述", is_required = False),
        'status': BooleanField(desc = "角色状态(0, 1)", is_required = False),
        'is_show_data': BooleanField(desc = "是否展示下级数据(0, 1)", is_required = False),
        'is_show_all': BooleanField(desc = "是否展示所有数据(0, 1)", is_required = False),
        'is_security': BooleanField(desc = "是否开启数据安全(0, 1)", is_required = False),
    })

    response = with_metaclass(ResponseFieldSet)

    @classmethod
    def get_desc(cls):
        return "添加角色接口"

    @classmethod
    def get_author(cls):
        return "fsy"

    def execute(self, request):
        RoleServer.is_name_exist(request.role_info['name'])
        RoleServer.add(**request.role_info)

    def fill(self, response):
        return response


class List(StaffAuthorizedApi):
    """获取角色列表"""
    request = with_metaclass(RequestFieldSet)

    response = with_metaclass(ResponseFieldSet)
    response.data_list = ResponseField(ListField, desc = '角色列表', fmt = DictField(desc = "角色列表", conf = {
        'id': IntField(desc = "角色id"),
        'name': CharField(desc = "角色名称"),
        'parent_id': IntField(desc = "上级角色id"),
        'describe': CharField(desc = "角色描述"),
        'status': BooleanField(desc = "角色状态(0, 1)"),
        'update_time': DatetimeField(desc = "角色最后一次编辑时间"),
    }))

    @classmethod
    def get_desc(cls):
        return "角色列表接口"

    @classmethod
    def get_author(cls):
        return "fsy"

    def execute(self, request):
        role_list = role_middleware.get_all_list()
        return role_list

    def fill(self, response, role_list):
        data_list = [{
            'id': role.id,
            'name': role.name,
            'parent_id': role.parent_id,
            'describe': role.describe,
            'status': role.status,
            'update_time': role.update_time,
        } for role in role_list]
        response.data_list = data_list
        return response

class Get(StaffAuthorizedApi):
    """角色详情"""
    request = with_metaclass(RequestFieldSet)
    request.role_id = RequestField(IntField, desc = '角色id')

    response = with_metaclass(ResponseFieldSet)
    response.role_info = ResponseField(DictField, desc = "角色信息", conf = {
        'id': IntField(desc = "角色id"),
        'name': CharField(desc = "角色名称"),
        'parent_id': IntField(desc = "上级角色id"),
        'describe': CharField(desc = "角色描述"),
        'status': BooleanField(desc = "角色状态(0, 1)"),
        'is_show_data': BooleanField(desc = "是否显示下级数据(0, 1)"),
        'is_show_all': BooleanField(desc = "是否显示所有数据(0, 1)"),
        'is_security': BooleanField(desc = "是否开启数据安全(0, 1)"),
        'rules': CharField(desc = "权限")
    })

    @classmethod
    def get_desc(cls):
        return "角色详情接口"

    @classmethod
    def get_author(cls):
        return "fsy"

    def execute(self, request):
        role = role_middleware.get_self(request.role_id)
        return role

    def fill(self, response , role):
        response.role_info = {
            'id': role.id,
            'name': role.name,
            'parent_id': role.parent_id,
            'describe': role.describe,
            'status': role.status,
            'is_show_data': role.is_show_data,
            'is_show_all': role.is_show_all,
            'is_security': role.is_security,
            'rules': role.rules
        }
        return response


class Update(StaffAuthorizedApi):
    """编辑角色"""
    request = with_metaclass(RequestFieldSet)
    request.role_id = RequestField(IntField, desc = '角色id')
    request.role_info = RequestField(DictField, desc = "角色信息", conf = {
        'name': CharField(desc = "角色名称"),
        'parent_id': IntField(desc = "上级角色id"),
        'describe': CharField(desc = "角色描述", is_required = False),
        'status': BooleanField(desc = "角色状态(0, 1)", is_required = False),
        'is_show_data': BooleanField(desc = "是否展示下级数据(0, 1)", is_required = False),
        'is_show_all': BooleanField(desc = "是否可查看所有数据(0, 1)", is_required = False),
        'is_security': BooleanField(desc = "是否开启数据安全(0, 1)", is_required = False),
        'rules': CharField(desc = "权限", is_required = False)
    })

    response = with_metaclass(ResponseFieldSet)

    @classmethod
    def get_desc(cls):
        return "编辑角色接口"

    @classmethod
    def get_author(cls):
        return "fsy"

    def execute(self, request):
        role = RoleServer.get(request.role_id)
        RoleServer.is_name_exist(request.role_info['name'], role)
        RoleServer.update(role, **request.role_info)

    def fill(self, response):
        return response


class Remove(StaffAuthorizedApi):
    """删除角色"""
    request = with_metaclass(RequestFieldSet)
    request.role_id = RequestField(IntField, desc = "角色id")

    response = with_metaclass(ResponseFieldSet)

    @classmethod
    def get_desc(cls):
        return "角色删除接口"

    @classmethod
    def get_author(cls):
        return "fsy"

    def execute(self, request):
        RoleServer.remove(request.role_id)

    def fill(self, response):
        return response
