# coding=UTF-8

from tuoen.abs.middleware.extend.sms.template.base import TemplateBase


class VerifyCodeSMS(TemplateBase):

    def get_label(self):
        return 'verify_code'

    def get_name(self):
        return '验证码'

    def get_params(self, code):
        return {'code': code}

    def verify_unique_no(self, *args, **kwargs):
        return True


verify_code_sms = VerifyCodeSMS()


class VerifyCodeAgentWithdrawSMS(TemplateBase):

    def get_label(self):
        return 'verify_code_agent_withdraw'

    def get_name(self):
        return '代理商提现验证码'

    def get_params(self, code):
        return {'code': code}

    def verify_unique_no(self, *args, **kwargs):
        return True


verify_code_agent_withdraw_sms = VerifyCodeAgentWithdrawSMS()


class VerifyCodeAgentSMS(TemplateBase):

    def get_label(self):
        return 'verify_code_agent'

    def get_name(self):
        return '代理商验证码'

    def get_params(self, code):
        return {'code': code}

    def verify_unique_no(self, *args, **kwargs):
        return True


verify_code_agent_sms = VerifyCodeAgentSMS()


class VerifyCodeAgentInviteSMS(TemplateBase):

    def get_label(self):
        return 'verify_code_agent_invite'

    def get_name(self):
        return '代理商邀请码'

    def get_params(self, code):
        return {'code': code}

    def verify_unique_no(self, *args, **kwargs):
        return True


verify_code_agent_invite_sms = VerifyCodeAgentInviteSMS()
