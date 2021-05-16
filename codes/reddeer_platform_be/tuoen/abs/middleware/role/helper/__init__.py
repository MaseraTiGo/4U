# coding=UTF-8

from tuoen.sys.utils.common.single import Single
from tuoen.abs.middleware.role.helper.platform import PlatformRoleHelper
from tuoen.abs.middleware.role.helper.agent import AgentRoleHelper


class RoleRegister(Single):

    def __init__(self):
        self._role_mapping = {}
        self._role_list = []

    def register_product(self, role_cls):
        self._role_mapping[role_cls.get_flag()] = role_cls

    def get_role_mapping(self):
        return self._role_mapping


role_register = RoleRegister()
role_register.register_product(PlatformRoleHelper())
role_register.register_product(AgentRoleHelper())
