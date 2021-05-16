# coding=UTF-8
import json
import random
from tuoen.sys.log.base import logger
from .base import SmsBase
# from tuoen.abs.middleware.ssocheck import local_sms_middleware
from tuoen.sys.utils.common.utils import generate_sn


class LocalSms(SmsBase):

    def get_label(self):
        return 'local_sms'

    def get_name(self):
        return '本地短信平台'

    def get_sign_name(self):
        from tuoen.abs.middleware.config import config_middleware
        return config_middleware.get_value(self.label, 'sign_name')

    def get_app_key(self):
        from tuoen.abs.middleware.config import config_middleware
        return config_middleware.get_value(self.label, 'app_key')

    def send(self, phone, template_id, template, sign_name, **kwargs):
        data_info = {'mobile': phone}
        data_info.update(kwargs)
        kwargs.update({
            'appKey': self.get_app_key(),
            'smsType': template_id,
            'channelCode': 'CHL_003',
            'requestId': generate_sn('SC'),
            'extendData': json.dumps([data_info])
        })
        result = local_sms_middleware.send_sms(**kwargs)
        if result.get('status') == 'ok':
            return True
        logger.error('短信发送失败，原因：{reason}'.format(reason = result.get('msg', '')))
        return False

    def get_nonce_str(self, length = 32):
        chars = "abcdefghijklmnopqrstuvwxyz0123456789"
        nonce_str = ""
        for i in range(length):
            tmp_len = random.randint(0, len(chars) - 1)
            nonce_str += chars[tmp_len:tmp_len + 1]
        return nonce_str


local_sms = LocalSms()
