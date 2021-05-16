# coding=UTF-8

from tuoen.abs.middleware.extend.sms.config.base import Config
from tuoen.abs.middleware.extend.sms.template.order import pre_order_send_sms


class LocalConfig(Config):
    classify = 'local_sms'

    templates = [pre_order_send_sms]

    @property
    def platform_classify(self):
        return self.classify, '本地短信配置'

    @property
    def use_templates(self):
        return self.templates

    @property
    def config_details_mapping(self):
        return {
            (self.classify, 'app_key', '短信app_key'): {},
            (self.classify, 'sign_name', '签名'): {},
            (self.classify, 'numebr', '次数'): {'default': '0'},
            (self.classify, 'pre_str', '前缀'): {'default': 'NO.'},
            (self.classify, pre_order_send_sms.label, '模板id'): {},
            (self.classify, "is_open", '短信开关'): {'default': 'no', 'type': 'select',
                                                 'option': ['yes', 'no']},
        }


local_config = LocalConfig()
