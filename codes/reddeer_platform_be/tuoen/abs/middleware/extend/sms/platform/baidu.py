# coding=UTF-8

from tuoen.abs.middleware.extend.sms.controller.baidu import baidu_sms
from tuoen.abs.middleware.extend.sms.config import baidu_config
from tuoen.abs.middleware.extend.sms.platform.base import SMSPlatform


class BaiduPlatform(SMSPlatform):
    label = 'baidu_sms'


baidu_platform = BaiduPlatform(baidu_sms, baidu_config)
