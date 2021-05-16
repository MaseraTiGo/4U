# coding=UTF-8

from tuoen.abs.middleware.extend.sms.platform.aliplatform import ali_platform
from tuoen.abs.middleware.extend.sms.platform.baidu import baidu_platform
from tuoen.abs.middleware.extend.sms.platform.haoservice import hao_service_platform
from tuoen.abs.middleware.extend.sms.platform.local import local_platform
from tuoen.abs.middleware.extend.sms.platform.netease import net_ease_platform
from tuoen.abs.middleware.extend.sms.platform.tencent import tencent_platform
from tuoen.sys.core.exception.business_error import BusinessError
from tuoen.sys.utils.common.single import Single


class SMSPlatformRepo(Single):
    platforms_mapping = {}

    @property
    def all_platforms(self):
        return self.platforms_mapping

    @property
    def all_controllers(self):
        controller_mapping = {}
        for label, rel_platform in self.platforms_mapping.items():
            controller_mapping[label] = rel_platform.controller
        return controller_mapping

    def get_platform_by_label(self, label):
        platform = self.platforms_mapping.get(label)
        if not platform:
            raise BusinessError('标签%s对应的平台不存在！' % label)
        return platform

    def add_platform(self, platform):
        self.platforms_mapping[platform.label] = platform

    @property
    def all_templates_mapping(self):
        templates = []
        for _, platform in self.platforms_mapping.items():
            templates.extend(platform.templates)
        templates = set(templates)
        return {
            template.label: template for template in templates
        }


sms_platform_repo = SMSPlatformRepo()

sms_platform_repo.add_platform(ali_platform)
sms_platform_repo.add_platform(baidu_platform)
sms_platform_repo.add_platform(net_ease_platform)
sms_platform_repo.add_platform(tencent_platform)
sms_platform_repo.add_platform(local_platform)
sms_platform_repo.add_platform(hao_service_platform)
