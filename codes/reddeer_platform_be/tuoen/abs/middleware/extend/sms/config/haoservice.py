# coding=UTF-8

from tuoen.abs.middleware.extend.sms.config.base import Config
from tuoen.abs.middleware.extend.sms.template.code import verify_code_sms, verify_code_agent_withdraw_sms, \
    verify_code_agent_sms, verify_code_agent_invite_sms
from tuoen.abs.middleware.extend.sms.template.order import order_send_sms, order_receive_sms, pre_order_send_sms
from tuoen.abs.middleware.extend.sms.template.customer import register_remind_sms, return_remind_sms, card_remind_sms


class HaoServiceConfig(Config):
    classify = 'haoservice_sms'

    templates = [verify_code_sms, order_send_sms, order_receive_sms, return_remind_sms, register_remind_sms,
                     card_remind_sms, verify_code_agent_sms,
                     verify_code_agent_invite_sms, verify_code_agent_withdraw_sms]

    @property
    def platform_classify(self):
        return self.classify, 'HaoService短信配置'

    @property
    def use_templates(self):
        return self.templates

    @property
    def config_details_mapping(self):
        return {
            (self.classify, 'key', '短信key'): {},
            (self.classify, 'is_open', '是否启用'): {'default': 'no', 'type': 'select', 'option': ['yes', 'no']},
            (self.classify, 'sign_name', '签名'): {},
            (self.classify, 'agent_sign_name', '代理商签名'): {},
            (self.classify, 'leshua_sign_name', '乐刷签名'): {},
            (self.classify, verify_code_agent_sms.label, '代理商验证码模板id'): {},
            (self.classify, verify_code_agent_withdraw_sms.label, '代理商提现验证码模板id'): {},
            (self.classify, verify_code_agent_invite_sms.label, '代理商邀请码模板id'): {},
            (self.classify, verify_code_sms.label, '验证码模板id'): {},
            (self.classify, order_send_sms.label, '发货短信模板id'): {},
            (self.classify, order_receive_sms.label, '签收短信模板id'): {},
            (self.classify, register_remind_sms.label, '注册提醒激活短行模板id'): {},
            (self.classify, return_remind_sms.label, '未刷到提示激活短信模板id'): {},
            (self.classify, card_remind_sms.label, '没有流水提示刷卡短信模板id'): {},
        }


hao_service_config = HaoServiceConfig()
