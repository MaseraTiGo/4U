# coding=UTF-8

from tuoen.abs.middleware.extend.sms.template.base import TemplateBase
from model.store.model_sms import Sms, StatusTypes


class RegisterRemindSMS(TemplateBase):

    def get_label(self):
        return 'register_remind'

    def get_name(self):
        return '注册提醒激活'

    def get_params(self, name, money):
        return {'name': name, 'money': money}

    def verify_unique_no(self, phone, euqipment_sn, *args, **kwargs):
        sms = Sms.objects.filter(unique_no=euqipment_sn, phone=phone, status=StatusTypes.SUCCESS, scene=self.label)
        return False if sms else True


register_remind_sms = RegisterRemindSMS()


class ReturnRemindSMS(TemplateBase):

    def get_label(self):
        return 'return_remind'

    def get_name(self):
        return '未刷到提示激活'

    def get_params(self, name, money):
        return {'name': name, 'money': money}

    def verify_unique_no(self, phone, euqipment_sn, *args, **kwargs):
        sms = Sms.objects.filter(unique_no=euqipment_sn, phone=phone, status=StatusTypes.SUCCESS, scene=self.label)
        return False if sms else True


return_remind_sms = ReturnRemindSMS()


class CardRemindSMS(TemplateBase):

    def get_label(self):
        return 'card_remind'

    def get_name(self):
        return '没有流水提示刷卡'

    def get_params(self, name, day):
        return {'name': name, 'day': day}

    def verify_unique_no(self, phone, euqipment_sn, *args, **kwargs):
        sms = Sms.objects.filter(unique_no=euqipment_sn, phone=phone, status=StatusTypes.SUCCESS, scene=self.label)
        return False if sms else True


card_remind_sms = CardRemindSMS()
