# coding=UTF-8

import datetime
import hashlib

from tuoen.abs.agent_service.role.manager import AgentRoleServer
from tuoen.abs.platform_service.account.manager import PlatformAccountServer
from tuoen.abs.agent_service.account.manager import AgentAccountServer
from tuoen.abs.platform_service.account.token import JwtGenerator
from tuoen.abs.platform_service.company.manager import CompanyServer
from tuoen.agile.base import NoAuthrizedApi
from tuoen.agile.platform_apis.base import PlatformAccountAuthorizedApi
from tuoen.sys.core.api.request import RequestField, RequestFieldSet
from tuoen.sys.core.api.response import ResponseField, ResponseFieldSet
from tuoen.sys.core.api.utils import with_metaclass
from tuoen.sys.core.exception.business_error import BusinessError
from tuoen.sys.core.field.base import CharField, DictField, ListField, BooleanField, IntField, DatetimeField


class Login(NoAuthrizedApi):
    """登录"""
    request = with_metaclass(RequestFieldSet)
    request.username = RequestField(CharField, desc="登录名")
    request.password = RequestField(CharField, desc="登录密码")

    response = with_metaclass(ResponseFieldSet)

    response.account_info = ResponseField(DictField, desc="账号信息", conf={
        'id': IntField(desc='账户id'),
        'username': CharField(desc='用户名'),
        'name': CharField(desc='联系人姓名'),
        'phone': CharField(desc='联系电话'),
        'is_main': BooleanField(desc='是否为主账号'),
        'role': CharField(desc='账号角色'),
        'rule_list': ListField(desc='权限列表', fmt=CharField('权限')),
        'last_login_time': DatetimeField(desc='最后一次登录时间')
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
        return 1001

    def execute(self, request):
        account = PlatformAccountServer.login(request.username, request.password)
        token = JwtGenerator.generate_jwt(account).decode('utf-8')
        return token, account

    def fill(self, response, token, account):
        response.auth_token = token
        response.account_info = {
            'id': account.id,
            'username': account.username,
            'name': account.name,
            'phone': account.phone,
            'is_main': account.is_main,
            'role': account.role.name if account.role else '',
            'rule_list': account.role.rules if account.role else [],
            'last_login_time': account.last_login_time
        }
        return response


class GenerateAgentAccount(PlatformAccountAuthorizedApi):
    """生成机构账号"""
    request = with_metaclass(RequestFieldSet)
    request.account_info = RequestField(DictField, desc="账号详情", conf={
        'username': CharField(desc="账号"),
        'password': CharField(desc="账号密码(加密后)"),
        'name': CharField(desc="姓名", is_required=False),
        'phone': CharField(desc="联系电话"),
        'company_name': CharField(desc='机构名称'),
        'company_phone': CharField(desc='机构电话', is_required=False),
        'company_address': CharField(desc='机构地址', is_required=False),
        'status': IntField(desc="账号状态：enable-启用-1，disable-停用-0", is_required=False),
    })

    response = with_metaclass(ResponseFieldSet)

    @classmethod
    def get_desc(cls):
        return "机构账号创建接口"

    @classmethod
    def get_author(cls):
        return "djd"

    @classmethod
    def get_protocol_num(cls):
        return 1002

    def execute(self, request):
        cur_account = self.load_auth_account()
        if not cur_account.is_main:
            raise BusinessError('该账号无添加机构权限')

        agent_account = AgentAccountServer.get_account_by_username(request.account_info["username"])
        if agent_account:
            raise BusinessError('该账号已存在')

        company = CompanyServer.create_while_initial(**request.account_info)

        if not company:
            raise BusinessError('该机构不存在')

        role = AgentRoleServer.create_admin_role_4_company(company)
        if not role:
            raise BusinessError('角色添加失败')

        request.account_info.update({
            'company': company,
            'is_main': True,
            'role': role,
        })

        agent_account = PlatformAccountServer.generate_agent_main_account(**request.account_info)
        if not agent_account:
            raise BusinessError('机构主账户创建失败')

    def fill(self, response):
        return response


class AgentAccountList(PlatformAccountAuthorizedApi):
    """机构账号"""
    request = with_metaclass(RequestFieldSet)
    request.current_page = RequestField(IntField, desc='页码')
    request.query_info = RequestField(DictField, desc='查询关键字', conf={
        'keywords': CharField(desc='查询关键字', is_required=False)
    })

    response = with_metaclass(ResponseFieldSet)
    response.account_info = ResponseField(ListField, desc="主账号列表", fmt=DictField(
        desc="主账号信息", conf={
            'id': IntField(desc='id'),
            'username': CharField(desc="账号"),
            'name': CharField(desc="姓名"),
            'phone': CharField(desc="联系电话"),
            'company_name': CharField(desc='公司名称'),
            'company_phone': CharField(desc='机构电话'),
            'company_addr': CharField(desc='机构唯一标识符'),
            'status': IntField(desc="账号状态：enable-启用-1，disable-停用-0"),
        }
    ))

    response.total = ResponseField(IntField, desc='总数')
    response.total_page = ResponseField(IntField, desc='总页数')

    @classmethod
    def get_desc(cls):
        return "机构账号查询接口"

    @classmethod
    def get_author(cls):
        return "djd"

    @classmethod
    def get_protocol_num(cls):
        return 1003

    def execute(self, request):
        cur_account = self.load_auth_account()
        if not cur_account.is_main:
            raise BusinessError('该账号无查询机构权限')
        agent_main_counts = PlatformAccountServer.search(
            request.current_page,
            **request.query_info
        )
        return agent_main_counts

    def fill(self, response, agent_main_counts):
        response.account_info = [{
            'id': account.id,
            'username': account.username,
            'company_name': account.company.name if account.company else '',
            'company_phone': account.company.phone if account.company else '',
            'company_addr': account.company.address if account.company else '',
            'name': account.name,
            'phone': account.phone,
            'status': account.status
        }
            for account in agent_main_counts.data
        ]

        response.total = agent_main_counts.total
        response.total_page = agent_main_counts.total_page
        return response


class StatusReverse(PlatformAccountAuthorizedApi):
    """更改主账号状态"""
    request = with_metaclass(RequestFieldSet)
    request.account_id = RequestField(IntField, desc='账号id')

    response = with_metaclass(ResponseFieldSet)

    @classmethod
    def get_desc(cls):
        return "更改主账号状态(停用|启用)接口"

    @classmethod
    def get_author(cls):
        return "djd"

    @classmethod
    def get_protocol_num(cls):
        return 1004

    def execute(self, request):
        if not self.auth_account.is_main:
            raise BusinessError('此账号无管理权限')

        agent_account = AgentAccountServer.get_account_by_id(request.account_id)
        if not agent_account.is_main:
            raise BusinessError('修改的账号存在异常')

        PlatformAccountServer.status_reverse(agent_account)

    def fill(self, response):
        return response


class Delete(PlatformAccountAuthorizedApi):
    """删除主账号"""
    request = with_metaclass(RequestFieldSet)
    request.account_id = RequestField(IntField, desc='账号id')

    response = with_metaclass(ResponseFieldSet)

    @classmethod
    def get_desc(cls):
        return "删除主账号接口"

    @classmethod
    def get_author(cls):
        return "djd"

    @classmethod
    def get_protocol_num(cls):
        return 1005

    def execute(self, request):
        if not self.auth_account.is_main:
            raise BusinessError('此账号无管理权限')

        PlatformAccountServer.delete(request.account_id)

    def fill(self, response):
        return response


class ResetAgentPwd(PlatformAccountAuthorizedApi):
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
        return 1006

    def execute(self, request):
        sub_accounts = PlatformAccountServer.reset_agent_password(request.account_id)
        return sub_accounts

    def fill(self, response):
        return response


class EditAgentAccount(PlatformAccountAuthorizedApi):
    """编辑机构账号"""
    request = with_metaclass(RequestFieldSet)
    request.account_id = RequestField(IntField, desc='账户id')
    request.edit_info = RequestField(DictField, desc="账号详情", conf={
        'company_name': CharField(desc='机构名称'),
        'name': CharField(desc="联系人", is_required=False),
        'phone': CharField(desc="联系电话"),
        'company_phone': CharField(desc='机构电话', is_required=False),
        'company_address': CharField(desc='机构地址', is_required=False),
        'status': IntField(desc="账号状态：enable-启用-1，disable-停用-0", is_required=False),
    })

    response = with_metaclass(ResponseFieldSet)

    @classmethod
    def get_desc(cls):
        return "机构账号修改接口"

    @classmethod
    def get_author(cls):
        return "djd"

    @classmethod
    def get_protocol_num(cls):
        return 1007

    def execute(self, request):
        # 待优化
        agent_account = AgentAccountServer.get_account_by_id(request.account_id)
        if not agent_account.is_main:
            raise BusinessError("机构账号存在异常")
        company_update_info = {}
        if "company_name" in request.edit_info:
            company_update_info["name"] = request.edit_info.pop("company_name")
        if "company_phone" in request.edit_info:
            company_update_info["phone"] = request.edit_info.pop("company_phone")
        if "company_address" in request.edit_info:
            company_update_info["address"] = request.edit_info.pop("company_address")
        status = request.edit_info.pop('status')
        if agent_account.status != status:
            PlatformAccountServer.status_reverse(agent_account)
            agent_account.status = status
        AgentAccountServer.update_account(agent_account, **request.edit_info)
        CompanyServer.update(agent_account.company, **company_update_info)

    def fill(self, response):
        return response


class ChangePassword(PlatformAccountAuthorizedApi):
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
        return 1008

    def execute(self, request):
        PlatformAccountServer.modify_password(self.auth_account, request.old_password, request.new_password)

    def fill(self, response):
        return response
