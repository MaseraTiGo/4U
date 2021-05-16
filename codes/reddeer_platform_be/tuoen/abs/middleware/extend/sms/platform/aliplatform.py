# coding=UTF-8

from tuoen.abs.middleware.extend.sms.controller.ali import ali_sms
from tuoen.abs.middleware.extend.sms.config import ali_config
from tuoen.abs.middleware.extend.sms.platform.base import SMSPlatform


class AliPlatform(SMSPlatform):
    label = 'ali_sms'


ali_platform = AliPlatform(ali_sms, ali_config)
