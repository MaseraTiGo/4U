# coding=UTF-8

from tuoen.abs.middleware.extend.sms.controller.haoservice import hao_service
from tuoen.abs.middleware.extend.sms.config import hao_service_config
from tuoen.abs.middleware.extend.sms.platform.base import SMSPlatform


class HaoServicePlatform(SMSPlatform):
    label = 'haoservice_sms'


hao_service_platform = HaoServicePlatform(hao_service, hao_service_config)
