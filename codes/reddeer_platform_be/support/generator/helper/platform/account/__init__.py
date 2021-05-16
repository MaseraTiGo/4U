# coding=UTF-8

import hashlib
import random
from support.generator.base import BaseGenerator
from support.generator.helper.platform.role import PlatformRoleGenerator
from model.store.model_account import PlatformAccount


class PlatformAccountGenerator(BaseGenerator):

    def __init__(self, platform_account_info):
        super(PlatformAccountGenerator, self).__init__()
        self._platform_account_infos = self.init(platform_account_info)

    def get_create_list(self, result_mapping):
        platform_role_list = result_mapping.get(PlatformRoleGenerator.get_key())
        for platform_account_info in self._platform_account_infos:
            platform_account_info.is_main = False
            platform_account_info.role = 0
            platform_account_info.password = hashlib.md5("123456".encode('utf8')).hexdigest()
            if platform_account_info.username == "admin":
                platform_account_info.is_main = True
                for platform_role in platform_role_list:
                    if platform_role.name == "超级管理员":
                        platform_account_info.role = platform_role
            else:
                platform_account_info.role = random.choice(platform_role_list)

        return self._platform_account_infos

    def create(self, platform_account_info, result_mapping):
        platform_account_qs = PlatformAccount.search(
            username=platform_account_info.username
        )
        if platform_account_qs.count():
            platform_account = platform_account_qs[0]
        else:
            platform_account = PlatformAccount.create(**platform_account_info)
        return platform_account

    def delete(self):
        print('==================>>> delete platform_account <======================')
        return None
