# coding=UTF-8

from model.store.model_role import PlatformRole
from support.generator.base import BaseGenerator


class PlatformRoleGenerator(BaseGenerator):

    def __init__(self, platform_role_info):
        super(PlatformRoleGenerator, self).__init__()
        self._platform_role_infos = self.init(platform_role_info)

    def get_create_list(self, result_mapping):
        return self._platform_role_infos

    def create(self, platform_role_info, result_mapping):
        platform_role_qs = PlatformRole.search(name=platform_role_info.name)
        if platform_role_qs.count():
            platform_role = platform_role_qs[0]
        else:
            platform_role = PlatformRole.create(**platform_role_info)
        return platform_role

    def delete(self):
        print('======================>>> delete platform_role <======================')
        return None
