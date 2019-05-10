# coding=UTF-8

'''
Created on 2016年7月22日

@author: Administrator
'''

from django.db.models import *
from django.utils import timezone
from model.base import BaseModel
from model.store.model_merchant import Merchant
from model.store.model_equipment_sn import EquipmentSn


class MerchantEquipment(BaseModel):
    """商户设备关系表"""
    merchant = ForeignKey(Merchant, on_delete=CASCADE)
    equipment_sn = ForeignKey(EquipmentSn, null=True, on_delete=CASCADE)
    serial_no = CharField(verbose_name="设备硬件序列号", max_length=256, default="")
    terminal_id = CharField(verbose_name="终端编号", max_length=256, default="")
    binding_date = DateTimeField(verbose_name="绑定时间", null=True, blank=True)

    update_time = DateTimeField(verbose_name="更新时间", auto_now=True)
    create_time = DateTimeField(verbose_name="创建时间", default=timezone.now)

    @classmethod
    def search(cls, **attrs):
        merchant_qs = cls.query().filter(**attrs)
        return merchant_qs
