# coding=UTF-8

from support.generator.helper.platform import *
from support.common.maker import BaseMaker


class PlatformAccountMaker(BaseMaker):

    def __init__(self, account_info, role_info):
        self._role = PlatformRoleGenerator(role_info)
        self._account = PlatformAccountGenerator(account_info)

    def generate_relate(self):
        self._account.add_inputs(self._role)
        return self._account
