# coding=UTF-8

from model.store.model_sms import Sms, StatusTypes
from tuoen.abs.middleware.extend.sms.template.base import TemplateBase


class OrderReceiveSMS(TemplateBase):

    def get_label(self):
        return 'order_receive'

    def get_name(self):
        return '签收'

    def get_params(self, name):
        return {'name': name}

    def verify_unique_no(self, phone, logistics_number, *args, **kwargs):
        sms = Sms.objects.filter(unique_no=logistics_number, phone=phone, status=StatusTypes.SUCCESS, scene=self.label)
        return False if sms else True


order_receive_sms = OrderReceiveSMS()


class OrderSendSMS(TemplateBase):

    def get_label(self):
        return 'order_send'

    def get_name(self):
        return '发货'

    def get_params(self, name, company, number):
        return {'name': name, 'company': company, 'number': number}

    def verify_unique_no(self, phone, logistics_number, *args, **kwargs):
        sms = Sms.objects.filter(unique_no=logistics_number, phone=phone, status=StatusTypes.SUCCESS, scene=self.label)
        return False if sms else True


order_send_sms = OrderSendSMS()


class PreOrderSendSMS(TemplateBase):
    def get_label(self):
        return 'pre_order_send'

    def get_name(self):
        return '推送售后微信号'

    def get_params(self, server_id):
        return {'serverId': server_id}

    def verify_unique_no(self, *args, **kwargs):
        return True


pre_order_send_sms = PreOrderSendSMS()
