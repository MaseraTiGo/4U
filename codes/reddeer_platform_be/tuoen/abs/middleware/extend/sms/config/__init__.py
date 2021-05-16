# coding=UTF-8

from tuoen.abs.middleware.extend.sms.config.ali import ali_config
from tuoen.abs.middleware.extend.sms.config.baidu import baidu_config
from tuoen.abs.middleware.extend.sms.config.common import common_config
from tuoen.abs.middleware.extend.sms.config.haoservice import hao_service_config
from tuoen.abs.middleware.extend.sms.config.local import local_config
from tuoen.abs.middleware.extend.sms.config.netease import net_ease_config
from tuoen.abs.middleware.extend.sms.config.tencent import tencent_config
from tuoen.sys.utils.common.single import Single


class SMSPlatformConfigRepo(Single):
    platform_configs = []

    @classmethod
    def add_platform_config(cls, platform_config):
        cls.platform_configs.append(platform_config)

    @property
    def all_platform_configs(self):
        return self.platform_configs


sms_platform_config_repo = SMSPlatformConfigRepo()

sms_platform_config_repo.add_platform_config(common_config)
sms_platform_config_repo.add_platform_config(ali_config)
sms_platform_config_repo.add_platform_config(hao_service_config)
sms_platform_config_repo.add_platform_config(tencent_config)
sms_platform_config_repo.add_platform_config(net_ease_config)
sms_platform_config_repo.add_platform_config(baidu_config)
sms_platform_config_repo.add_platform_config(local_config)
