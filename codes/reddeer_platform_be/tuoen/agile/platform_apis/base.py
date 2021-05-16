# -*- coding: UTF-8 -*-    
# Author: Dongjd
# FileName: base
# DateTime: 2020/12/18 9:42
# Project: awesome_dong
# Do Not Touch Me!

from tuoen.abs.platform_service.account.manager import PlatformAccountServer
from tuoen.abs.platform_service.role.manager import PlatformRoleServer
from tuoen.agile.base import BaseAccountAuthorizedApi


class PlatformAccountAuthorizedApi(BaseAccountAuthorizedApi):
    AccountServer = PlatformAccountServer
    RoleServer = PlatformRoleServer
    FLAG = 'admin'
