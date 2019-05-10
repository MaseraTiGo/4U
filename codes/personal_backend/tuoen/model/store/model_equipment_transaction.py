# coding=UTF-8

'''
Created on 2016年7月22日

@author: Administrator
'''

from django.db.models import *
from django.utils import timezone
from model.base import BaseModel
from model.store.model_equipment_register import EquipmentRegister


class EquipmentTransaction(BaseModel):
    """交易流水表"""

    agent_name = CharField(verbose_name = "代理商名称", max_length = 32, default = "", null = True)
    service_code = CharField(verbose_name = "服务编码", max_length = 32, default = "", null = True)
    register_code = CharField(verbose_name = "客户编码", max_length = 32, null = False, default = "")
    code = ForeignKey(EquipmentRegister, null = True, on_delete=CASCADE)
    phone = CharField(verbose_name = "注册手机号", max_length = 32, default = "", null = True)
    transaction_time = DateTimeField(verbose_name = "交易日期", default = timezone.now)
    transaction_code = CharField(verbose_name = "交易流水号", max_length = 32, default = "", null = True)
    transaction_money = IntegerField(verbose_name = "交易金额/分", default = 0)
    fee = IntegerField(verbose_name = "手续费/分", default = 0)
    good_service_fee = IntegerField(verbose_name = "优享手续费/分", default = 0)
    rate = IntegerField(verbose_name = "客户费率", default = 0)
    good_service_rate = IntegerField(verbose_name = "优享费率", default = 0)
    other_fee = IntegerField(verbose_name = "其它手续费/分", default = 0)
    transaction_status = CharField(verbose_name = "交易状态", max_length = 64, default = "", null = True)
    type = CharField(verbose_name = "号段类型", max_length = 64, default = "", null = True)

    update_time = DateTimeField(verbose_name = "更新时间", auto_now = True)
    create_time = DateTimeField(verbose_name = "创建时间", default = timezone.now)

    @classmethod
    def search(cls, **attrs):
        equipment_register_qs = cls.query().filter(**attrs)
        return equipment_register_qs

    @classmethod
    def sum_money(cls, **attrs):
        equipment_register_qs = cls.search(**attrs)
        equipment_register_qs = equipment_register_qs.values("code").annotate(sum_transaction_money = Sum('transaction_money'))
        if len(equipment_register_qs) > 0:
            return equipment_register_qs[0]["sum_transaction_money"]
        else:
            return 0
