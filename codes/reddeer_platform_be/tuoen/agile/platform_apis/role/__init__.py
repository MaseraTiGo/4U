# -*- coding: UTF-8 -*-    
# Author: Dongjd
# FileName: __init__.py
# DateTime: 2020/12/10 16:32
# Project: operate_backend_be
# Do Not Touch Me!

# from tuoen.abs.platform_service.company.manager import CompanyServer
# from tuoen.abs.platform_service.role.manager import PlatformRoleServer
# from tuoen.agile.platform_apis.base import PlatformAccountAuthorizedApi
# from tuoen.sys.core.api.request import RequestField, RequestFieldSet
# from tuoen.sys.core.api.response import ResponseField, ResponseFieldSet
# from tuoen.sys.core.api.utils import with_metaclass
# from tuoen.sys.core.exception.business_error import BusinessError
# from tuoen.sys.core.field.base import CharField, DictField, ListField, IntField


# class List(PlatformAccountAuthorizedApi):
#     """角色列表"""
#
#     request = with_metaclass(RequestFieldSet)
#     request.current_page = RequestField(IntField, desc="页码")
#
#     response = with_metaclass(ResponseFieldSet)
#
#     response.role_list = ResponseField(ListField, desc="角色列表", fmt=DictField(
#         desc="角色信息", conf={
#             'id': IntField(desc="id"),
#             'name': CharField(desc="角色名"),
#             'status': CharField(desc="账户状态"),
#         }
#     ))
#
#     response.total = ResponseField(IntField, desc="总数")
#     response.total_page = ResponseField(IntField, desc="总页数")
#
#     @classmethod
#     def get_desc(cls):
#         return "角色列表接口"
#
#     @classmethod
#     def get_author(cls):
#         return "djd"
#
#     @classmethod
#     def get_protocol_num(cls):
#         return 2001
#
#     def execute(self, request):
#         roles = PlatformRoleServer.search(request.current_page)
#         return roles
#
#     def fill(self, response, roles):
#         response.role_list = [
#             {
#                 'id': role.id,
#                 'name': role.name,
#                 'status': role.status
#             }
#             for role in roles.data
#         ]
#         response.total = roles.total
#         response.total_page = roles.total_page
#
#         return response
#
#
# class Create(PlatformAccountAuthorizedApi):
#     """创建"""
#
#     request = with_metaclass(RequestFieldSet)
#     request.create_info = RequestField(DictField, desc="新建", conf={
#         'name': CharField(desc="角色名"),
#         'status': CharField(desc="账户状态", is_required=False),
#         'rules': CharField(desc="功能权限"),
#         'describe': CharField(desc='描述', is_required=False),
#     })
#
#     response = with_metaclass(ResponseFieldSet)
#
#     @classmethod
#     def get_desc(cls):
#         return "角色创建接口"
#
#     @classmethod
#     def get_author(cls):
#         return "djd"
#
#     @classmethod
#     def get_protocol_num(cls):
#         return 2002
#
#     def execute(self, request):
#
#         role = PlatformRoleServer.create_role(**request.create_info)
#         if not role:
#             raise BusinessError('角色创建失败')
#
#     def fill(self, response):
#         return response
#
#
# class StatusReverse(PlatformAccountAuthorizedApi):
#     """角色状态转换"""
#
#     request = with_metaclass(RequestFieldSet)
#     request.role_id = RequestField(IntField, desc="role ID")
#
#     response = with_metaclass(ResponseFieldSet)
#
#     response.occupy_list = ResponseField(ListField, desc="角色占用列表", fmt=CharField(
#         desc="角色信息",
#     ))
#
#     @classmethod
#     def get_desc(cls):
#         return "角色列表接口"
#
#     @classmethod
#     def get_author(cls):
#         return "djd"
#
#     @classmethod
#     def get_protocol_num(cls):
#         return 2003
#
#     def execute(self, request):
#         accounts = PlatformRoleServer.status_reverse(request.role_id)
#         return accounts
#
#     def fill(self, response, accounts):
#         response.occupy_list = accounts
#         return response
#
#
# class Delete(PlatformAccountAuthorizedApi):
#     """角色删除"""
#
#     request = with_metaclass(RequestFieldSet)
#     request.role_id = RequestField(IntField, desc="role ID")
#
#     response = with_metaclass(ResponseFieldSet)
#
#     @classmethod
#     def get_desc(cls):
#         return "角色列表接口"
#
#     @classmethod
#     def get_author(cls):
#         return "djd"
#
#     @classmethod
#     def get_protocol_num(cls):
#         return 2004
#
#     def execute(self, request):
#         accounts = PlatformRoleServer.delete_role_by_id(request.role_id)
#         return accounts
#
#     def fill(self, response, accounts):
#         response.occupy_list = accounts
#         return response
