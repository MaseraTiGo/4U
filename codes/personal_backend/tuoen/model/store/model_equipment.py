# coding=UTF-8

'''
Created on 2016年7月22日

@author: Administrator
'''

from django.db.models import *
from django.utils import timezone
from model.base import BaseModel
from model.store.model_mobilephone import Mobilephone
from model.store.model_product import Product, ProductModel
from model.store.model_logistics import LogisticsItem
from model.store.model_customer import Customer
from model.store.model_order import Order


class EquipmentStatusType(object):
    RED = 'red'
    YELLOW = 'yellow'
    GREEN = 'green'
    TGREEB = 'tgreen'

    CHOICES = ((RED, '红'), (YELLOW, '黄'), (GREEN, "绿"), (TGREEB, "双绿"))

class EquipmentStatusState(object):
    NORMAL = 'normal'
    REPLACE = 'replace'
    PATCH = 'patch'
    RGOODS = 'rgoods'
    ABNORMAL = 'abnormal'
    STATUS = ((NORMAL, "正常"), (REPLACE, "售后机"), (PATCH, "补货"), (RGOODS, "注册并退货"), (ABNORMAL, "异常"))

class Equipment(BaseModel):
    """设备表"""
    customer = ForeignKey(Customer, null = True, on_delete=CASCADE)
    logistics_item = ForeignKey(LogisticsItem, null = True, on_delete=CASCADE)
    order = ForeignKey(Order, null = True, on_delete=CASCADE)
    product = ForeignKey(Product, null = True, on_delete=CASCADE)
    product_model = ForeignKey(ProductModel, null = True, on_delete=CASCADE)
    code = CharField(verbose_name = "设备编码", max_length = 64)    
    equipment_status = CharField(verbose_name = "设备状态", max_length = 64, choices = EquipmentStatusState.STATUS, \
                                default = EquipmentStatusState.NORMAL)
    last_cal_time = DateTimeField(verbose_name = "最后统计时间", max_length = 20, null = True, blank = True)
    total_amount = IntegerField(verbose_name = "交易总额/分", default = 0)

    update_time = DateTimeField(verbose_name = "更新时间", auto_now = True)
    create_time = DateTimeField(verbose_name = "创建时间", default = timezone.now)

    @classmethod
    def search(cls, **attrs):
        equipment_qs = cls.query().filter(**attrs)
        return equipment_qs
