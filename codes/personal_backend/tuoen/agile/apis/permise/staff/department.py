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
from tuoen.abs.middleware.department import department_middleware
from tuoen.abs.service.permise.manager import DepartmentServer


class Add(StaffAuthorizedApi):
    """添加部门"""
    request = with_metaclass(RequestFieldSet)
    request.department_info = RequestField(DictField, desc = "部门详情", conf = {
        'name': CharField(desc = "部门名称"),
        'parent_id': IntField(desc = "上级部门id"),
        'describe': CharField(desc = "部门描述", is_required = False),
    })

    response = with_metaclass(ResponseFieldSet)

    @classmethod
    def get_desc(cls):
        return "添加部门接口"

    @classmethod
    def get_author(cls):
        return "fsy"

    def execute(self, request):
        DepartmentServer.is_name_exist(request.department_info['name'])
        DepartmentServer.add(**request.department_info)

    def fill(self, response):
        return response


class List(StaffAuthorizedApi):
    """获取部门列表"""
    request = with_metaclass(RequestFieldSet)


    response = with_metaclass(ResponseFieldSet)
    response.data_list = ResponseField(ListField, desc = '部门列表', fmt = DictField(desc = "部门列表", conf = {
        'id': IntField(desc = "部门id"),
        'name': CharField(desc = "部门名称"),
        'parent_id': IntField(desc = "上级部门id"),
        'parent_name': CharField(desc = "上级部门名称"),
        'describe': CharField(desc = "部门描述"),
        'status': BooleanField(desc = "部门状态(0, 1)"),
        'update_time': DatetimeField(desc = "部门最后一次编辑时间"),
    }))

    @classmethod
    def get_desc(cls):
        return "部门列表接口"

    @classmethod
    def get_author(cls):
        return "fsy"

    def execute(self, request):
        department_list = department_middleware.get_all_list()
        return department_list

    def fill(self, response, department_list):
        data_list = [{
            'id': department.id,
            'name': department.name,
            'parent_id': department.parent_id,
            'parent_name': department.parent_id,
            'describe': department.describe,
            'status': department.status,
            'update_time': department.update_time,
        } for department in department_list]
        response.data_list = data_list
        return response


class Get(StaffAuthorizedApi):
    """部门详情"""
    request = with_metaclass(RequestFieldSet)
    request.department_id = RequestField(IntField, desc = '部门id')

    response = with_metaclass(ResponseFieldSet)
    response.department_info = ResponseField(DictField, desc = "部门信息", conf = {
        'id': IntField(desc = "部门id"),
        'name': CharField(desc = "部门名称"),
        'parent_id': IntField(desc = "上级部门id"),
        'describe': CharField(desc = "部门描述"),
    })

    @classmethod
    def get_desc(cls):
        return "部门详情接口"

    @classmethod
    def get_author(cls):
        return "fsy"

    def execute(self, request):
        department = department_middleware.get_self(request.department_id)
        return department

    def fill(self, response , department):
        response.department_info = {
            'id': department.id,
            'name': department.name,
            'parent_id': department.parent_id,
            'describe': department.describe,
        }
        return response


class Update(StaffAuthorizedApi):
    """编辑部门"""
    request = with_metaclass(RequestFieldSet)
    request.department_id = RequestField(IntField, desc = '部门id')
    request.department_info = RequestField(DictField, desc = "部门信息", conf = {
        'name': CharField(desc = "部门名称"),
        'parent_id': IntField(desc = "上级部门id"),
        'describe': CharField(desc = "部门描述", is_required = False),
    })

    response = with_metaclass(ResponseFieldSet)

    @classmethod
    def get_desc(cls):
        return "编辑部门接口"

    @classmethod
    def get_author(cls):
        return "fsy"

    def execute(self, request):
        department = DepartmentServer.get(request.department_id)
        DepartmentServer.is_name_exist(request.department_info['name'], department)
        DepartmentServer.update(department, **request.department_info)

    def fill(self, response):
        return response


class Remove(StaffAuthorizedApi):
    """删除部门"""
    request = with_metaclass(RequestFieldSet)
    request.department_id = RequestField(IntField, desc = "部门id")

    response = with_metaclass(ResponseFieldSet)

    @classmethod
    def get_desc(cls):
        return "部门删除接口"

    @classmethod
    def get_author(cls):
        return "fsy"

    def execute(self, request):
        DepartmentServer.remove(request.department_id)

    def fill(self, response):
        return response
