# coding=UTF-8

from tuoen.abs.middleware.extend.sms.controller.local import local_sms
from tuoen.abs.middleware.extend.sms.config import local_config
from tuoen.abs.middleware.extend.sms.platform.base import SMSPlatform


class LocalPlatform(SMSPlatform):
    label = 'local_sms'


local_platform = LocalPlatform(local_sms, local_config)
