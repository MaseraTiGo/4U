# -*- coding: UTF-8 -*-    
# Author: Dongjd
# FileName: __init__.py
# DateTime: 2020/12/10 14:37
# Project: operate_backend_be
# Do Not Touch Me!

import json

from model.store.model_account import AgentAccount
from model.store.model_role import AgentRole
from tuoen.abs.common_service.role import RoleServerBase
from tuoen.abs.middleware.rule import RuleMiddleware
from tuoen.sys.core.exception.business_error import BusinessError
from tuoen.abs.middleware.role import role_middleware


class AgentRoleServer(RoleServerBase):
    RoleModel = AgentRole
    AccountModel = AgentAccount
    RelativesAccounts = 'role_agent_accounts'

    @classmethod
    def is_role_used(cls, role):
        role_relative_accounts = getattr(role, cls.RelativesAccounts).all()
        role_relative_accounts = role_relative_accounts.exclude(status=AgentAccount.Status.DELETE)
        if role_relative_accounts:
            raise BusinessError('角色在使用中， 不能停用')

    @classmethod
    def status_reverse(cls, role_id):
        accounts = []
        role = cls.get_role_by_id(role_id)
        if role.status == cls.RoleModel.Status.ENABLE:
            cls.is_role_used(role)
            role.update(**{'status': cls.RoleModel.Status.DISABLE})
        else:
            role.update(**{'status': cls.RoleModel.Status.ENABLE})
        return accounts

    @classmethod
    def edit_role(cls, role_id, **edit_info):
        role = cls.RoleModel.search(name=edit_info.get('name'), company=edit_info.get('company')).first()
        if role and role.id != role_id and role.status != cls.RoleModel.Status.DELETE:
            raise BusinessError('角色已存在')
        role = cls.get_role_by_id(role_id)
        if not edit_info.get('status', 1):
            cls.is_role_used(role)
        role.update(**edit_info)
        # 更新缓存
        role_middleware.set_redis(cls.RoleModel.__name__.lower(), role)

    @classmethod
    def list_classified_by_company(cls, company):
        return AgentRole.search(company=company, status=AgentRole.Status.ENABLE)

    @classmethod
    def is_role_valid(cls, role):
        return role.status == AgentRole.Status.ENABLE
