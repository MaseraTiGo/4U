# coding=UTF-8

import datetime

from tuoen.abs.agent_service.account.manager import AgentAccountServer
from tuoen.abs.agent_service.account.token import JwtGenerator
from tuoen.abs.agent_service.role.manager import AgentRoleServer
from tuoen.agile.agent_apis.base import AgentAccountAuthorizedApi
from tuoen.agile.base import NoAuthrizedApi
from tuoen.sys.core.api.request import RequestField, RequestFieldSet
from tuoen.sys.core.api.response import ResponseField, ResponseFieldSet
from tuoen.sys.core.api.utils import with_metaclass
from tuoen.sys.core.exception.business_error import BusinessError
from tuoen.sys.core.field.base import CharField, DictField, ListField, BooleanField, IntField


class Login(NoAuthrizedApi):
    """登录"""
    request = with_metaclass(RequestFieldSet)
    request.username = RequestField(CharField, desc="登录名")
    request.password = RequestField(CharField, desc="登录密码")

    response = with_metaclass(ResponseFieldSet)

    response.account_info = ResponseField(DictField, desc="账号信息", conf={
        'id': IntField(desc='账号id'),
        'is_main': BooleanField(desc='是否为主账号'),
        'company_name': CharField(desc='机构名称'),
        'username': CharField(desc='账户名'),
        'name': CharField(desc='联系人'),
        'phone': CharField(desc='联系人电话'),
        'company_phone': CharField(desc='机构电话'),
        'company_addr': CharField(desc='机构地址'),
        'role': CharField(desc='账号角色'),
        'rule_list': ListField(desc='权限列表', fmt=CharField('权限'))
    })

    response.auth_token = ResponseField(CharField, desc="用户访问令牌")

    @classmethod
    def get_desc(cls):
        return "登录接口"

    @classmethod
    def get_author(cls):
        return "djd"

    @classmethod
    def get_protocol_num(cls):
        return 100001

    def execute(self, request):
        account = AgentAccountServer.login(request.username, request.password)
        token = JwtGenerator.generate_jwt(account).decode('utf-8')
        return token, account

    def fill(self, response, token, account):
        response.auth_token = token
        response.account_info = {
            'id': account.id,
            'is_main': account.is_main,
            'company_name': account.company.name if account.company else '',
            'username': account.username,
            'name': account.name,
            'phone': account.phone,
            'company_phone': account.company.phone if account.company else '',
            'company_addr': account.company.address if account.company else '',
            'role': account.role.name if account.role else '',
            'rule_list': account.role.rules if account.role else []
        }
        return response


class GenerateSubAccount(AgentAccountAuthorizedApi):
    """生成子账号"""
    request = with_metaclass(RequestFieldSet)
    request.account_info = RequestField(DictField, desc="账号详情", conf={
        'username': CharField(desc="账号"),
        'password': CharField(desc="密码(加密后)"),
        'name': CharField(desc="姓名"),
        'phone': CharField(desc="联系电话", is_required=False),
        'role_id': IntField(desc="角色id"),
        'status': IntField(desc="账号状态：enable-启用-1，disable-停用-0"),
    })

    response = with_metaclass(ResponseFieldSet)

    @classmethod
    def get_desc(cls):
        return "子账号创建接口"

    @classmethod
    def get_author(cls):
        return "djd"

    @classmethod
    def get_protocol_num(cls):
        return 100002

    def execute(self, request):
        cur_account = self.load_auth_account()
        role = AgentRoleServer.get_role_by_id(request.account_info.pop('role_id'))
        if role.company_id != cur_account.company_id:
            raise BusinessError("角色存在异常")
        if cur_account.is_main:
            prefix = cur_account.username
        else:
            prefix = cur_account.username.split("-")[0]
        username = prefix + '-' + request.account_info.pop("username")
        request.account_info['username'] = username

        request.account_info.update({
            'company': cur_account.company,
            'role': role,
            'last_login_time': datetime.datetime.now()
        })
        AgentAccountServer.generate_sub_account(**request.account_info)

    def fill(self, response):
        return response


class ChangePassword(AgentAccountAuthorizedApi):
    """修改密码"""
    request = with_metaclass(RequestFieldSet)
    request.old_password = RequestField(CharField, desc="加密后的登录密码")
    request.new_password = RequestField(CharField, desc="加密后的新登录密码")

    response = with_metaclass(ResponseFieldSet)

    @classmethod
    def get_desc(cls):
        return "修改密码接口"

    @classmethod
    def get_author(cls):
        return "djd"

    @classmethod
    def get_protocol_num(cls):
        return 100003

    def execute(self, request):
        AgentAccountServer.modify_password(self.auth_account, request.old_password, request.new_password)

    def fill(self, response):
        return response


class SubAccountList(AgentAccountAuthorizedApi):
    """子账号列表"""

    request = with_metaclass(RequestFieldSet)
    request.current_page = RequestField(IntField, desc="页码")

    response = with_metaclass(ResponseFieldSet)

    response.sub_account_list = ResponseField(ListField, desc="子账号列表", fmt=DictField(
        desc="子账号信息", conf={
            'id': IntField(desc="id"),
            'username': CharField(desc="登录账号"),
            'name': CharField(desc="姓名"),
            'phone': CharField(desc="联系电话"),
            'role_id': IntField(desc="角色id"),
            'role': CharField(desc="角色"),
            'status': IntField(desc="账户状态:账号状态：enable-启用-1，disable-停用-0"),
        }
    ))

    response.total = ResponseField(IntField, desc="总数")
    response.total_page = ResponseField(IntField, desc="总页数")

    @classmethod
    def get_desc(cls):
        return "子账号列表接口"

    @classmethod
    def get_author(cls):
        return "djd"

    @classmethod
    def get_protocol_num(cls):
        return 100004

    def execute(self, request):
        company = self.auth_account.company
        sub_accounts = AgentAccountServer.search_my_sub(request.current_page, **{'company': company})
        return sub_accounts

    def fill(self, response, sub_accounts):
        response.sub_account_list = [
            {
                'id': account.id,
                'username': account.username,
                'name': account.name,
                'phone': account.phone,
                'role_id': account.role.id,
                'role': account.role.name,
                'status': account.status
            }
            for account in sub_accounts.data
        ]
        response.total = sub_accounts.total
        response.total_page = sub_accounts.total_page

        return response


class UpdateAccount(AgentAccountAuthorizedApi):
    """编辑账号"""

    request = with_metaclass(RequestFieldSet)
    request.account_id = RequestField(IntField, desc="账户ID")
    request.update_info = RequestField(DictField, desc="编辑信息", conf={
        'username': CharField(desc="账户名称", is_required=False),
        'password': CharField(desc="已加密密码", is_required=False),
        'name': CharField(desc="姓名", is_required=False),
        'phone': CharField(desc="联系电话", is_required=False),
        'role_id': IntField(desc="角色id", is_required=False),
        'status': IntField(desc="账户状态:enable-启用-1，disable-停用-0", is_required=False),
    })

    response = with_metaclass(ResponseFieldSet)

    @classmethod
    def get_desc(cls):
        return "账户编辑接口"

    @classmethod
    def get_author(cls):
        return "djd"

    @classmethod
    def get_protocol_num(cls):
        return 100005

    def execute(self, request):
        cur_account = self.auth_account
        if 'role_id' in request.update_info:
            role = AgentRoleServer.get_role_by_id(request.update_info.pop('role_id'))
            if role.company_id != cur_account.company_id:
                raise BusinessError("角色存在异常")
            request.update_info.update({'role':role})
        if 'username' in request.update_info:
            if cur_account.is_main:
                prefix = cur_account.username
            else:
                prefix = cur_account.username.split("-")[0]
            username = prefix + '-' + request.update_info.pop("username")
            request.update_info['username'] = username
        account = AgentAccountServer.get_account_by_id(request.account_id)
        if cur_account.company_id != account.company_id:
            raise BusinessError("账户信息异常")
        AgentAccountServer.update_account(
            account,
            **request.update_info
        )

    def fill(self, response):
        return response


class StatusReverse(AgentAccountAuthorizedApi):
    """改变账户状态"""
    request = with_metaclass(RequestFieldSet)
    request.account_id = RequestField(IntField, desc="账户ID")

    response = with_metaclass(ResponseFieldSet)

    @classmethod
    def get_desc(cls):
        return "账户状态反转接口"

    @classmethod
    def get_author(cls):
        return "djd"

    @classmethod
    def get_protocol_num(cls):
        return 100006

    def execute(self, request):
        AgentAccountServer.status_reverse(request.account_id)

    def fill(self, response):
        return response


class ResetPwd(AgentAccountAuthorizedApi):
    """重置密码"""
    request = with_metaclass(RequestFieldSet)
    request.account_id = RequestField(IntField, desc="账户ID")

    response = with_metaclass(ResponseFieldSet)

    @classmethod
    def get_desc(cls):
        return "账户密码重置接口"

    @classmethod
    def get_author(cls):
        return "djd"

    @classmethod
    def get_protocol_num(cls):
        return 100007

    def execute(self, request):
        sub_accounts = AgentAccountServer.reset_password(request.account_id)
        return sub_accounts

    def fill(self, response):
        return response


class Delete(AgentAccountAuthorizedApi):
    """账户删除"""
    request = with_metaclass(RequestFieldSet)
    request.account_id = RequestField(IntField, desc="账户ID")

    response = with_metaclass(ResponseFieldSet)

    @classmethod
    def get_desc(cls):
        return "账户删除接口"

    @classmethod
    def get_author(cls):
        return "djd"

    @classmethod
    def get_protocol_num(cls):
        return 100008

    def execute(self, request):
        AgentAccountServer.delete(request.account_id)

    def fill(self, response):
        return response


class EditAccount(AgentAccountAuthorizedApi):
    """编辑账号"""

    request = with_metaclass(RequestFieldSet)
    request.account_id = RequestField(IntField, desc="账户ID")
    request.update_info = RequestField(DictField, desc="编辑信息", conf={
        'name': CharField(desc="联系人姓名", is_required=False),
        'phone': CharField(desc="机构电话|联系人电话", is_required=False),
        'address': CharField(desc="机构地址", is_required=False),
    })

    response = with_metaclass(ResponseFieldSet)

    @classmethod
    def get_desc(cls):
        return "账户编辑接口"

    @classmethod
    def get_author(cls):
        return "djd"

    @classmethod
    def get_protocol_num(cls):
        return 100009

    def execute(self, request):
        cur_account=self.auth_account
        AgentAccountServer.edit_account(cur_account, **request.update_info)

    def fill(self, response):
        return response


class AutoLogin(AgentAccountAuthorizedApi):
    """自动登录"""

    request = with_metaclass(RequestFieldSet)

    response = with_metaclass(ResponseFieldSet)
    response.account_info = ResponseField(DictField, desc="账号信息", conf={
        'id': IntField(desc='账号id'),
        'is_main': BooleanField(desc='是否为主账号'),
        'company_name': CharField(desc='机构名称'),
        'username': CharField(desc='账户名'),
        'name': CharField(desc='联系人'),
        'phone': CharField(desc='联系人电话'),
        'company_phone': CharField(desc='机构电话'),
        'company_addr': CharField(desc='机构地址'),
        'role': CharField(desc='账号角色'),
        'rule_list': ListField(desc='权限列表', fmt=CharField('权限'))
    })

    @classmethod
    def get_desc(cls):
        return "自动登录接口"

    @classmethod
    def get_author(cls):
        return "djd"

    @classmethod
    def get_protocol_num(cls):
        return 100010

    def execute(self, request):
        return self.auth_account

    def fill(self, response, account):

        response.account_info = {
            'id': account.id,
            'is_main': account.is_main,
            'company_name': account.company.name if account.company else '',
            'username': account.username,
            'name': account.name,
            'phone': account.phone,
            'company_phone': account.company.phone if account.company else '',
            'company_addr': account.company.address if account.company else '',
            'role': account.role.name if account.role else '',
            'rule_list': account.role.rules if account.role else []
        }

        return response


class Get(AgentAccountAuthorizedApi):
    """账户信息"""
    request = with_metaclass(RequestFieldSet)
    request.account_id = RequestField(IntField, desc="账户ID")

    response = with_metaclass(ResponseFieldSet)

    response.account_info = ResponseField(DictField, desc="账号信息", conf={
        'id': IntField(desc='账号id'),
        'is_main': BooleanField(desc='是否为主账号'),
        'company_name': CharField(desc='机构名称'),
        'username': CharField(desc='账户名'),
        'name': CharField(desc='联系人'),
        'phone': CharField(desc='联系人电话'),
        'company_phone': CharField(desc='机构电话'),
        'company_addr': CharField(desc='机构地址'),
        'role': CharField(desc='账号角色'),
        'rule_list': ListField(desc='权限列表', fmt=CharField('权限'))
    })

    @classmethod
    def get_desc(cls):
        return "获取账户信息接口"

    @classmethod
    def get_author(cls):
        return "djd"

    @classmethod
    def get_protocol_num(cls):
        return 100011

    def execute(self, request):
        account = AgentAccountServer.get_account_by_id(request.account_id)
        return account

    def fill(self, response, account):
        response.account_info = {
            'id': account.id,
            'is_main': account.is_main,
            'company_name': account.company.name if account.company else '',
            'username': account.username,
            'name': account.name,
            'phone': account.phone,
            'company_phone': account.company.phone if account.company else '',
            'company_addr': account.company.address if account.company else '',
            'role': account.role.name if account.role else '',
            'rule_list': account.role.rules if account.role else []
        }
        return response
