# coding=UTF-8

from support.common.maker import BaseMaker
from support.generator.helper.platform import *
from support.environment.maker.agent import *
from support.environment.init.agent.company import CompanyLoader
from support.environment.init.agent.role import RoleLoader
from support.environment.init.agent.account import AccountLoader


class AgentInitializeMaker(BaseMaker):
    """
    仅仅管理A端初始化的数据
    1、角色数据
    2、账号数据
    """

    def __init__(self):
        self._account = AgentAccountMaker(
            CompanyLoader().generate(),
            AccountLoader().generate(),
            RoleLoader().generate()
        ).generate_relate()

    def generate_relate(self):
        return self._account


if __name__ == "__main__":
    AgentInitializeMaker().run()
