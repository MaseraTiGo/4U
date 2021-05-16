# -*- coding: UTF-8 -*-    
# Author: Dongjd
# FileName: __init__.py
# DateTime: 2020/12/10 14:37
# Project: operate_backend_be
# Do Not Touch Me!

from model.store.model_role import PlatformRole
from model.store.model_account import PlatformAccount
from tuoen.abs.common_service.role import RoleServerBase


class PlatformRoleServer(RoleServerBase):
    RoleModel = PlatformRole
    AccountModel = PlatformAccount
    RelativesAccounts = 'role_platform_accounts'
