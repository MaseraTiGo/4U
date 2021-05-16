# coding=UTF-8

from support.common.maker import BaseMaker
from support.generator.helper.platform import *
from support.environment.maker.platform import *
from support.environment.init.platform.role import RoleLoader
from support.environment.init.platform.account import AccountLoader


class PlatformInitializeMaker(BaseMaker):
    """
    仅仅管理B端初始化的数据
    1、角色数据
    2、账号数据
    """

    def __init__(self):
        self._account = PlatformAccountMaker(
            AccountLoader().generate(),
            RoleLoader().generate()
        ).generate_relate()

    def generate_relate(self):
        return self._account


if __name__ == "__main__":
    PlatformInitializeMaker().run()
