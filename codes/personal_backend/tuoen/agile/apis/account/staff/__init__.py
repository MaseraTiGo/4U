# coding=UTF-8

# 环境的

# 第三方

# 公用的
from tuoen.sys.core.exception.business_error import BusinessError
from tuoen.sys.core.field.base import CharField, DictField, IntField, ListField, BooleanField, DatetimeField
from tuoen.sys.core.api.request import RequestField, RequestFieldSet
from tuoen.sys.core.api.utils import with_metaclass
from tuoen.sys.core.api.response import ResponseField, ResponseFieldSet

from tuoen.abs.middleware.role import role_middleware
from tuoen.abs.middleware.department import department_middleware
# 逻辑的  service | middleware - > apis
from tuoen.agile.apis.base import NoAuthrizedApi, StaffAuthorizedApi
from tuoen.abs.service.account.manager import StaffAccountServer
from tuoen.abs.service.user.manager import UserServer, StaffServer
from tuoen.abs.service.permise.manager import StaffPermiseServer


class Login(NoAuthrizedApi):
    """登录"""
    request = with_metaclass(RequestFieldSet)
    request.username = RequestField(CharField, desc="登录名")
    request.password = RequestField(CharField, desc="登录密码")
    request._ip = RequestField(CharField, desc="登陆IP")

    response = with_metaclass(ResponseFieldSet)
    response.auth_token = ResponseField(CharField, desc="用户访问令牌")
    response.renew_flag = ResponseField(CharField, desc="续签访问令牌标识")
    response.role_list = ResponseField(ListField, desc='角色列表', fmt=DictField(desc="角色列表", conf={
        'id': IntField(desc="角色id"),
        'name': CharField(desc="角色名称"),
        'parent_id': IntField(desc="上级角色id"),
        'describe': CharField(desc="角色描述"),
        'status': BooleanField(desc="角色状态(0, 1)"),
        'update_time': CharField(desc="角色最后一次编辑时间"),
    }))
    response.department_list = ResponseField(ListField, desc='部门列表', fmt=DictField(desc="部门列表", conf={
        'id': IntField(desc="部门id"),
        'name': CharField(desc="部门名称"),
        'parent_id': IntField(desc="上级部门id"),
        'parent_name': CharField(desc="上级部门名称"),
        'describe': CharField(desc="部门描述"),
        'status': BooleanField(desc="部门状态(0, 1)"),
        'update_time': CharField(desc="部门最后一次编辑时间"),
    }))
    response.rule_list = ResponseField(ListField, desc='功能列表', fmt=DictField(desc="功能列表", conf={
        'flag': CharField(desc="功能名称"),
    }))

    @classmethod
    def get_desc(cls):
        return "员工登录接口"

    @classmethod
    def get_author(cls):
        return "fsy"

    def execute(self, request):
        print('---------------->here', request.username, request.password, request._ip)
        staff_account = StaffAccountServer.login(request.username, request.password, request._ip)
        if staff_account:
            print('=============>get it')
        token = UserServer.generate_token(staff_account.staff)

        staff = staff_account.staff
        role_list = []
        department_list = []
        rule_list = []
        if staff.is_admin:
            role_list = role_middleware.get_all_list()
            department_list = department_middleware.get_all_list()
        else:
            role_list, department_list = StaffPermiseServer.get_myall_level(staff)
            rule_list = StaffPermiseServer.get_rules_bystaff(staff_account.staff)
            rule_list = list(set(rule_list))

        return token, role_list, department_list, rule_list

    def fill(self, response, token, role_list, department_list, rule_list):
        response.auth_token = token.auth_token
        response.renew_flag = token.renew_flag
        role_list = [{
            'id': role.id,
            'name': role.name,
            'parent_id': role.parent_id,
            'describe': role.describe,
            'status': role.status,
            'update_time': role.update_time,
        } for role in role_list]
        response.role_list = role_list
        department_list = [{
            'id': department.id,
            'name': department.name,
            'parent_id': department.parent_id,
            'parent_name': department.parent_id,
            'describe': department.describe,
            'status': department.status,
            'update_time': department.update_time,
        } for department in department_list]
        response.department_list = department_list
        rule_list = [{
            'flag': rule,
        } for rule in rule_list]
        response.rule_list = rule_list
        return response


class Generate(StaffAuthorizedApi):
    """给员工生成账号"""
    request = with_metaclass(RequestFieldSet)
    request.staff_id = RequestField(IntField, desc='员工id')
    request._ip = RequestField(CharField, desc="IP")
    request.account_info = RequestField(DictField, desc="账号详情", conf={
        'username': CharField(desc="账号"),
        'password': CharField(desc="密码", is_required=False),
        'status': CharField(desc="账号状态(enable:启用,lock:锁定,disable:禁用,notactive:待激活)"),
    })

    response = with_metaclass(ResponseFieldSet)

    @classmethod
    def get_desc(cls):
        return "给员工生成账号或修改接口"

    @classmethod
    def get_author(cls):
        return "fsy"

    def execute(self, request):
        staff = StaffServer.get(request.staff_id)
        StaffAccountServer.register_account_bystaff(staff, request._ip, **request.account_info)

    def fill(self, response):
        return response
