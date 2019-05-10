# coding=UTF-8

'''
Created on 2016年7月22日

@author: Administrator
'''

from django.db.models import *
from django.utils import timezone
from model.base import BaseModel
from model.store.model_user import Staff
from model.store.model_customer import Customer
from model.store.model_shop import Shop, Goods


class SaleChance(BaseModel):
    """客户机会表"""
    customer = ForeignKey(Customer, on_delete=CASCADE)
    staff = ForeignKey(Staff, null = True, on_delete=CASCADE)
    shop = ForeignKey(Shop, null = True, on_delete=CASCADE)
    goods = ForeignKey(Goods, null = True, on_delete=CASCADE)
    remark = TextField(verbose_name = "备注", default = "")
    order_count = IntegerField(verbose_name = "订单总数", default = 0)
    order_ids = TextField(verbose_name = "订单id", default = "[]")

    end_time = DateField(verbose_name = "机会截至时间", max_length = 20, null = False, blank = False)

    update_time = DateTimeField(verbose_name = "更新时间", auto_now = True)
    create_time = DateTimeField(verbose_name = "创建时间", default = timezone.now)

    @classmethod
    def search(cls, **attrs):
        sale_chance_qs = cls.query().filter(**attrs)
        return sale_chance_qs
