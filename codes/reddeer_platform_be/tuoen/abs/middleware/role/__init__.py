# coding=UTF-8

from tuoen.sys.utils.common.single import Single
from tuoen.sys.core.exception.business_error import BusinessError
from tuoen.abs.middleware.role.helper import role_register


class RoleMiddleware(Single):
    _role_mapping = {}

    def __init__(self):
        self._role_mapping = role_register.get_role_mapping()

    def check_role_flag(self, role_flag):
        if role_flag not in self._role_mapping:
            raise BusinessError("此角色类型不存在")

    def set_redis(self, role_flag, role):
        self.check_role_flag(role_flag)
        self._role_mapping[role_flag].set_redis(role)
        return True

    def get_redis(self, role_flag, role_id):
        self.check_role_flag(role_flag)
        value = self._role_mapping[role_flag].get_redis(role_id)
        return value

    def delete_redis(self, role_flag, role_id):
        self.check_role_flag(role_flag)
        self._role_mapping[role_flag].delete_redis(role_id)
        return True


role_middleware = RoleMiddleware()
