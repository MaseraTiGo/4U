# coding=UTF-8

'''
Created on 2016年7月22日

@author: Administrator
'''

from django.db.models import *
from django.utils import timezone
from model.base import BaseModel
from model.store.model_customer import Customer
from model.store.model_order import Order, OrderItem


class Logistics(BaseModel):
    order = ForeignKey(Order, on_delete=CASCADE)
    customer = ForeignKey(Customer, on_delete=CASCADE)

    company = CharField(verbose_name = "物流公司", max_length = 64, default = "", null = True)
    number = CharField(verbose_name = "物流单号", max_length = 64, default = "", null = True)
    total_quantity = IntegerField(verbose_name = "发货数量")

    update_time = DateTimeField(verbose_name = "更新时间", auto_now = True)
    create_time = DateTimeField(verbose_name = "创建时间", default = timezone.now)


class LogisticsItem(BaseModel):
    customer = ForeignKey(Customer, on_delete=CASCADE)
    logistics = ForeignKey(Logistics, on_delete=CASCADE)

    order_item = ForeignKey(OrderItem, on_delete=CASCADE)
    quantity = IntegerField(verbose_name = "数量")

    equipment_sn_list = TextField(verbose_name = "sn码列表", default = "[]")

    update_time = DateTimeField(verbose_name = "更新时间", auto_now = True)
    create_time = DateTimeField(verbose_name = "创建时间", default = timezone.now)
