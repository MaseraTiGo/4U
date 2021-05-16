# coding=UTF-8

from tuoen.abs.middleware.extend.sms.config.base import Config
from tuoen.abs.middleware.extend.sms.template.code import verify_code_sms, verify_code_agent_withdraw_sms, \
    verify_code_agent_sms, verify_code_agent_invite_sms
from tuoen.abs.middleware.extend.sms.template.order import order_send_sms, order_receive_sms, pre_order_send_sms
from tuoen.abs.middleware.extend.sms.template.customer import register_remind_sms, return_remind_sms, card_remind_sms


class CommonConfig(Config):
    classify = 'common_sms'

    templates = [verify_code_sms, order_send_sms, order_receive_sms, return_remind_sms, register_remind_sms,
                     card_remind_sms, verify_code_agent_sms,
                     verify_code_agent_invite_sms, verify_code_agent_withdraw_sms, pre_order_send_sms]

    @property
    def platform_classify(self):
        return self.classify, '短信通用配置'

    @property
    def use_templates(self):
        return self.templates

    @property
    def config_details_mapping(self):
        return {
            (self.classify, 'sms_label', '验证码短信平台label'): {},
            (self.classify, verify_code_sms.label + '_is_open', '验证码短信开关'): {'default': 'no', 'type': 'select',
                                                                             'option': ['yes', 'no']},
            (self.classify, verify_code_sms.label + '_content', '验证码短信内容'): {},
            (self.classify, verify_code_agent_sms.label + '_content', '代理商验证码短信内容'): {},
            (self.classify, verify_code_agent_withdraw_sms.label + '_content', '代理商提现验证码短信内容'): {},
            (self.classify, verify_code_agent_invite_sms.label + '_content', '代理商邀请码短信内容'): {},
            (self.classify, order_send_sms.label + '_is_open', '发货短信开关'): {'default': 'no', 'type': 'select',
                                                                           'option': ['yes', 'no']},
            (self.classify, order_send_sms.label + '_content', '发货短信内容'): {},
            (self.classify, order_receive_sms.label + '_is_open', '签收短信开关'): {'default': 'no', 'type': 'select',
                                                                              'option': ['yes', 'no']},
            (self.classify, order_receive_sms.label + '_content', '签收短信内容'): {},
            (self.classify, register_remind_sms.label + '_is_open', '注册提醒激活短信开关'): {'default': 'no', 'type': 'select',
                                                                                    'option': ['yes', 'no']},
            (self.classify, register_remind_sms.label + '_content', '注册提醒激活短行内容'): {},
            (self.classify, return_remind_sms.label + '_is_open', '未刷到提示激活短信开关'): {'default': 'no', 'type': 'select',
                                                                                   'option': ['yes', 'no']},
            (self.classify, return_remind_sms.label + '_content', '未刷到提示激活短信内容'): {},
            (self.classify, card_remind_sms.label + '_is_open', '没有流水提示刷卡短信开关'): {'default': 'no', 'type': 'select',
                                                                                  'option': ['yes', 'no']},
            (self.classify, card_remind_sms.label + '_content', '没有流水提示刷卡短信内容'): {},
            (self.classify, pre_order_send_sms.label + '_is_open', '预订单发短信开关'): {'default': 'no', 'type': 'select',
                                                                                 'option': ['yes', 'no']},
            (self.classify, pre_order_send_sms.label + '_content', '预订单发短信内容'): {'default': ''}
        }


common_config = CommonConfig()
