# coding=UTF-8

from tuoen.abs.middleware.extend.sms.controller.netease import netease_sms
from tuoen.abs.middleware.extend.sms.config import net_ease_config
from tuoen.abs.middleware.extend.sms.platform.base import SMSPlatform


class NetEasePlatform(SMSPlatform):
    label = 'netease_sms'


net_ease_platform = NetEasePlatform(netease_sms, net_ease_config)
