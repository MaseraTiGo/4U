# -*- coding: UTF-8 -*-    
# Author: Dongjd
# FileName: __init__.py
# DateTime: 2020/12/10 16:32
# Project: operate_backend_be
# Do Not Touch Me!

from tuoen.abs.agent_service.role.manager import AgentRoleServer
from tuoen.agile.agent_apis.base import AgentAccountAuthorizedApi
from tuoen.sys.core.api.request import RequestField, RequestFieldSet
from tuoen.sys.core.api.response import ResponseField, ResponseFieldSet
from tuoen.sys.core.api.utils import with_metaclass
from tuoen.sys.core.field.base import CharField, DictField, ListField, IntField, NewDictField


class Search(AgentAccountAuthorizedApi):
    """角色列表"""

    request = with_metaclass(RequestFieldSet)
    request.current_page = RequestField(IntField, desc="页码")

    response = with_metaclass(ResponseFieldSet)

    response.role_list = ResponseField(ListField, desc="角色列表", fmt=DictField(
        desc="角色信息", conf={
            'id': IntField(desc="id"),
            'name': CharField(desc="角色名"),
            'rules': NewDictField(desc="角色对应权限"),
            'status': IntField(desc="账户状态:enable-启用-1，disable-停用-0"),
        }
    ))

    response.total = ResponseField(IntField, desc="总数")
    response.total_page = ResponseField(IntField, desc="总页数")

    @classmethod
    def get_desc(cls):
        return "角色列表接口"

    @classmethod
    def get_author(cls):
        return "djd"

    @classmethod
    def get_protocol_num(cls):
        return 200001

    def execute(self, request):
        company = self.auth_account.company
        roles = AgentRoleServer.search(request.current_page, company)
        return roles

    def fill(self, response, roles):
        response.role_list = [
            {
                'id': role.id,
                'name': role.name,
                'rules': role.rules,
                'status': role.status
            }
            for role in roles.data
        ]
        response.total = roles.total
        response.total_page = roles.total_page

        return response


class Edit(AgentAccountAuthorizedApi):
    """角色编辑"""

    request = with_metaclass(RequestFieldSet)
    request.role_id = RequestField(IntField, desc='角色ID')
    request.edit_info = RequestField(DictField, desc="新建|编辑", conf={
        'name': CharField(desc="角色名"),
        'status': IntField(desc="账户状态:enable-启用-1，disable-停用-0"),
        'rules': NewDictField(desc="功能权限"),
    })

    response = with_metaclass(ResponseFieldSet)

    @classmethod
    def get_desc(cls):
        return "角色编辑接口"

    @classmethod
    def get_author(cls):
        return "djd"

    @classmethod
    def get_protocol_num(cls):
        return 200002

    def execute(self, request):
        company = self.auth_account.company
        request.edit_info.update({'company': company})
        AgentRoleServer.edit_role(request.role_id, **request.edit_info)

    def fill(self, response):
        return response


class StatusReverse(AgentAccountAuthorizedApi):
    """角色状态转换"""

    request = with_metaclass(RequestFieldSet)
    request.role_id = RequestField(IntField, desc="role ID")
    # request.status = RequestField(IntField,
    #                               desc='状态id：状态:DISABLE = 0 ENABLE = 1 DELETE = 2 '
    #                                    '[(DISABLE, 停用), (ENABLE, 启用), (DELETE, 删除)]')

    response = with_metaclass(ResponseFieldSet)

    response.occupy_list = ResponseField(ListField, desc="角色占用列表", fmt=CharField(
        desc="角色信息",
    ))

    @classmethod
    def get_desc(cls):
        return "角色状态反转接口"

    @classmethod
    def get_author(cls):
        return "djd"

    @classmethod
    def get_protocol_num(cls):
        return 200003

    def execute(self, request):
        accounts = AgentRoleServer.status_reverse(request.role_id)
        return accounts

    def fill(self, response, accounts):
        response.occupy_list = accounts
        return response


class Delete(AgentAccountAuthorizedApi):
    """角色删除"""

    request = with_metaclass(RequestFieldSet)
    request.role_id = RequestField(IntField, desc="role ID")

    response = with_metaclass(ResponseFieldSet)

    @classmethod
    def get_desc(cls):
        return "角色删除接口"

    @classmethod
    def get_author(cls):
        return "djd"

    @classmethod
    def get_protocol_num(cls):
        return 200004

    def execute(self, request):
        accounts = AgentRoleServer.delete_role_by_id(request.role_id)
        return accounts

    def fill(self, response, accounts):
        response.occupy_list = accounts
        return response


class Create(AgentAccountAuthorizedApi):
    """角色创建"""

    request = with_metaclass(RequestFieldSet)
    request.create_info = RequestField(DictField, desc="新建", conf={
        'name': CharField(desc="角色名"),
        'status': IntField(desc="账户状态:enable-启用-1，disable-停用-0"),
        'rules': NewDictField(desc="功能权限"),
    })

    response = with_metaclass(ResponseFieldSet)

    @classmethod
    def get_desc(cls):
        return "角色创建接口"

    @classmethod
    def get_author(cls):
        return "djd"

    @classmethod
    def get_protocol_num(cls):
        return 200005

    def execute(self, request):
        request.create_info.update({
            'company': self.auth_account.company
        })
        AgentRoleServer.create_role(**request.create_info)

    def fill(self, response):
        return response


class List(AgentAccountAuthorizedApi):
    """可用角色列表"""

    request = with_metaclass(RequestFieldSet)

    response = with_metaclass(ResponseFieldSet)

    response.role_list = ResponseField(ListField, desc="角色列表", fmt=DictField(
        desc="角色信息", conf={
            'id': IntField(desc="id"),
            'name': CharField(desc="角色名"),
        }
    ))

    @classmethod
    def get_desc(cls):
        return "可用角色列表接口"

    @classmethod
    def get_author(cls):
        return "djd"

    @classmethod
    def get_protocol_num(cls):
        return 200006

    def execute(self, request):
        company = self.auth_account.company
        roles = AgentRoleServer.list_classified_by_company(company)
        return roles

    def fill(self, response, roles):
        response.role_list = [
            {
                'id': role.id,
                'name': role.name,
            }
            for role in roles
        ]

        return response
