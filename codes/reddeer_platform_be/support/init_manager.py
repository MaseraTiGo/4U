# coding=UTF-8

import init_envt

from tuoen.sys.utils.common.single import Single
from support.environment.init.platform import PlatformInitializeMaker
from support.environment.init.agent import AgentInitializeMaker


class InitManager(Single):

    @staticmethod
    def run():
        # B端初始化数据
        PlatformInitializeMaker().run()
        # A端初始化数据
        AgentInitializeMaker().run()


if __name__ == "__main__":
    InitManager().run()
