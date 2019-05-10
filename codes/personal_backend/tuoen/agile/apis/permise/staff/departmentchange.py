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
from tuoen.abs.service.permise.manager import DepartmentServer, DepartmentChangeServer
from tuoen.abs.service.user.manager import StaffServer


class Add(StaffAuthorizedApi):
    """添加部门调岗任务"""
    request = with_metaclass(RequestFieldSet)
    request.department_change_info = RequestField(DictField, desc = "部门调岗任务详情", conf = {
        'staff_id': IntField(desc = "员工id"),
        'department_front_id': IntField(desc = "原部门id", is_required = False),
        'department_now_id': IntField(desc = "现部门id"),
        "start_time":DatetimeField(desc = "开始时间", is_required = False),
        "end_time":DatetimeField(desc = "结束时间"),
        "remark":CharField(desc = "备注", is_required = False),
    })

    response = with_metaclass(ResponseFieldSet)

    @classmethod
    def get_desc(cls):
        return "添加部门调岗任务接口"

    @classmethod
    def get_author(cls):
        return "fsy"

    def execute(self, request):
        auth_user = self.auth_user
        request.department_change_info.update({"adder":auth_user})

        staff_id = request.department_change_info.pop("staff_id")
        staff = StaffServer.get(staff_id)
        request.department_change_info.update({"staff":staff})

        if "department_front_id" in request.department_change_info:
            department_front_id = request.department_change_info.pop("department_front_id")
            department_front = department_middleware.get_self(department_front_id)
            request.department_change_info.update({"department_front":department_front})

        department_now_id = request.department_change_info.pop("department_now_id")
        department_now = department_middleware.get_self(department_now_id)
        if department_now is None:
            raise BusinessError("该部门不存在")
        request.department_change_info.update({"department_now":department_now})
        DepartmentChangeServer.generate(**request.department_change_info)

    def fill(self, response):
        return response


class Search(StaffAuthorizedApi):
    """获取部门调岗任务列表"""
    request = with_metaclass(RequestFieldSet)
    request.current_page = RequestField(IntField, desc = "当前查询页码")
    request.search_info = RequestField(DictField, desc = '搜索条件', conf = {
        'keyword': CharField(desc = "关键词(可搜索员工姓名或者工号)", is_required = False)
    })

    response = with_metaclass(ResponseFieldSet)
    response.data_list = ResponseField(ListField, desc = '部门调岗任务列表', fmt = DictField(desc = "部门调岗任务列表", conf = {
        'id': IntField(desc = "部门调岗任务id"),
        'staff_id': IntField(desc = "员工id"),
        'staff_name': CharField(desc = "员工姓名"),
        'staff_number': CharField(desc = "员工工号"),
        'adder_name': CharField(desc = "添加者姓名"),
        'executor_name': CharField(desc = "执行者姓名"),
        'department_front_id': IntField(desc = "原部门id"),
        'department_front_name': CharField(desc = "原部门名称"),
        'department_now_id': IntField(desc = "现部门id"),
        'department_now_name': CharField(desc = "现部门名称"),
        'start_time': DatetimeField(desc = "调岗开始时间"),
        'end_time': DatetimeField(desc = "调岗结束时间"),
        'status': CharField(desc = "任务状态(unexecuted:未执行,executed:已执行)"),
        'remark': CharField(desc = "备注"),
        'create_time': DatetimeField(desc = "任务添加时间"),
    }))
    response.total = ResponseField(IntField, desc = "数据总数")
    response.total_page = ResponseField(IntField, desc = "总页码数")

    @classmethod
    def get_desc(cls):
        return "部门调岗任务列表接口"

    @classmethod
    def get_author(cls):
        return "fsy"

    def execute(self, request):
        department_change_list = DepartmentChangeServer.search(request.current_page, **request.search_info)
        return department_change_list

    def fill(self, response, department_change_list):
        response.data_list = [{
            'id': department_change.id,
            'staff_id': department_change.staff.id,
            'staff_name': department_change.staff.name,
            'staff_number': department_change.staff.number,
            'adder_name': department_change.adder.name if department_change.adder else "",
            'executor_name': department_change.executor.name if department_change.executor else "",
            'department_front_id': department_change.department_front.id if department_change.department_front else 0,
            'department_front_name': department_change.department_front.name if department_change.department_front else "",
            'department_now_id': department_change.department_now.id,
            'department_now_name': department_change.department_now.name,
            'start_time': department_change.start_time,
            'end_time': department_change.end_time,
            'status': department_change.status,
            'remark': department_change.remark,
            'create_time': department_change.create_time,
        } for department_change in department_change_list.data]
        response.total = department_change_list.total
        response.total_page = department_change_list.total_page
        return response


class Get(StaffAuthorizedApi):
    """部门调岗任务详情"""
    request = with_metaclass(RequestFieldSet)
    request.department_change_id = RequestField(IntField, desc = '部门调岗任务id')

    response = with_metaclass(ResponseFieldSet)
    response.department_change_info = ResponseField(DictField, desc = "部门调岗任务信息", conf = {
        'id': IntField(desc = "部门调岗任务id"),
        'staff_id': IntField(desc = "员工id"),
        'department_front_id': IntField(desc = "原部门id"),
        'department_now_id': IntField(desc = "现部门id"),
        'start_time': DatetimeField(desc = "调岗开始时间"),
        'end_time': DatetimeField(desc = "调岗结束时间"),
        'remark': CharField(desc = "备注"),
    })

    @classmethod
    def get_desc(cls):
        return "部门调岗任务详情接口"

    @classmethod
    def get_author(cls):
        return "fsy"

    def execute(self, request):
        department_change = DepartmentChangeServer.get(request.department_change_id)
        return department_change

    def fill(self, response , department_change):
        response.department_change_info = {
            'id': department_change.id,
            'staff_id': department_change.staff_id,
            'department_front_id': department_change.department_front_id,
            'department_now_id': department_change.department_now_id,
            'start_time': department_change.start_time,
            'end_time': department_change.end_time,
            'remark': department_change.remark,
        }
        return response


class Update(StaffAuthorizedApi):
    """编辑部门调岗任务"""
    request = with_metaclass(RequestFieldSet)
    request.department_change_id = RequestField(IntField, desc = '部门调岗任务id')
    request.department_change_info = RequestField(DictField, desc = "部门调岗任务信息", conf = {
        'staff_id': IntField(desc = "员工id"),
        'department_front_id': IntField(desc = "原部门id", is_required = False),
        'department_now_id': IntField(desc = "现部门id"),
        'start_time': DatetimeField(desc = "调岗开始时间", is_required = False),
        'end_time': DatetimeField(desc = "调岗结束时间"),
        'remark': CharField(desc = "备注", is_required = False),
    })

    response = with_metaclass(ResponseFieldSet)

    @classmethod
    def get_desc(cls):
        return "编辑部门调岗任务接口"

    @classmethod
    def get_author(cls):
        return "fsy"

    def execute(self, request):
        department_change = DepartmentChangeServer.get(request.department_change_id)

        auth_user = self.auth_user
        request.department_change_info.update({"adder":auth_user})

        staff_id = request.department_change_info.pop("staff_id")
        staff = StaffServer.get(staff_id)
        request.department_change_info.update({"staff":staff})

        if "department_front_id" in request.department_change_info:
            department_front_id = request.department_change_info.pop("department_front_id")
            department_front = department_middleware.get_self(department_front_id)
            request.department_change_info.update({"department_front":department_front})

        department_now_id = request.department_change_info.pop("department_now_id")
        department_now = department_middleware.get_self(department_now_id)
        if department_now is None:
            raise BusinessError("该部门不存在")
        request.department_change_info.update({"department_now":department_now})

        DepartmentChangeServer.update(department_change, **request.department_change_info)

    def fill(self, response):
        return response


class Remove(StaffAuthorizedApi):
    """删除部门调岗任务"""
    request = with_metaclass(RequestFieldSet)
    request.department_change_id = RequestField(IntField, desc = "部门调岗任务id")

    response = with_metaclass(ResponseFieldSet)

    @classmethod
    def get_desc(cls):
        return "部门调岗任务删除接口"

    @classmethod
    def get_author(cls):
        return "fsy"

    def execute(self, request):
        department_change = DepartmentChangeServer.get(request.department_change_id)
        DepartmentChangeServer.remove(department_change)

    def fill(self, response):
        return response

class Executed(StaffAuthorizedApi):
    """执行部门调岗任务"""
    request = with_metaclass(RequestFieldSet)
    request.department_change_id = RequestField(IntField, desc = "部门调岗任务id")

    response = with_metaclass(ResponseFieldSet)

    @classmethod
    def get_desc(cls):
        return "部门调岗任务执行接口"

    @classmethod
    def get_author(cls):
        return "fsy"

    def execute(self, request):
        auth_user = self.auth_user
        department_change = DepartmentChangeServer.get(request.department_change_id)
        DepartmentChangeServer.executed(department_change, auth_user)

    def fill(self, response):
        return response

