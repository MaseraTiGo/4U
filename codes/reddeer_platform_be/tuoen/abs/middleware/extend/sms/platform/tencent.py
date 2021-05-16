# coding=UTF-8

from tuoen.abs.middleware.extend.sms.controller.tencent import tencent_sms
from tuoen.abs.middleware.extend.sms.config import tencent_config
from tuoen.abs.middleware.extend.sms.platform.base import SMSPlatform


class TencentPlatform(SMSPlatform):
    label = 'tencent_sms'


tencent_platform = TencentPlatform(tencent_sms, tencent_config)
