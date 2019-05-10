# coding=UTF-8

'''
Created on 2016年7月22日

@author: Administrator
'''

from django.db.models import *
from django.utils import timezone
from model.base import BaseModel
from model.store.model_order import Order
from model.models import Staff, Department
from model.store.model_event_base import EventBase
from model.store.model_equipment import Equipment
from model.store.model_customer import Customer
from model.store.model_shop import Goods

class Restatus(object):
    WAITING = 'wait'
    EXPORT = 'export'
    DONE = 'done'
    RESEND = "resend"
    CHOICE = ((WAITING, '待补货'), (EXPORT, '已导出'), (DONE, '已完成'), (RESEND, '补货中'))

class ReplenishmentNum(object):
    @property
    def replenishment_num(self):
        import time
        import random
        prefix = 'BF'
        time_mark = str(int(time.time()))
        rand_num = str(random.randint(1000, 9999))
        replenishment_num = prefix + time_mark + rand_num
        return replenishment_num

class Replenishment(BaseModel):
    order = ForeignKey(Order, null = True, on_delete=CASCADE)
    customer = ForeignKey(Customer, null = True, on_delete=CASCADE)
    replenishment_num = CharField(verbose_name = "补货單號", max_length = 64, default = "")
    quantity = IntegerField(verbose_name = "数量", default = 0)
    remark = CharField(verbose_name = "備註", max_length = 128, default = "")
    update_time = DateTimeField(verbose_name = "更新时间", auto_now = True)
    create_time = DateTimeField(verbose_name = "创建时间", default = timezone.now)

    @classmethod
    def search(cls, **attrs):
        replenishment_qs = cls.query().filter(**attrs)
        return replenishment_qs

class ReplenishmentItem(BaseModel):
    replenishment = ForeignKey(Replenishment, on_delete=CASCADE)
    code = ForeignKey(Equipment, on_delete=CASCADE)
    goods = ForeignKey(Goods, on_delete=CASCADE)
    remark = CharField(verbose_name="備註", max_length = 128, default="")
    status = CharField(verbose_name="补货状态", max_length=64, choices=Restatus.CHOICE, default='')
    amount = IntegerField(verbose_name="金额", default=0)
    update_time = DateTimeField(verbose_name="更新时间", auto_now=True)
    create_time = DateTimeField(verbose_name="创建时间", default=timezone.now)

    @classmethod
    def search(cls, **attrs):
        replenishment_item_qs = cls.query().filter(**attrs)
        return replenishment_item_qs

class ReplenishmentEvent(EventBase):
    replenishment = ForeignKey(Replenishment, on_delete=CASCADE)
    describe = TextField(verbose_name = "描述", null = True, default = "")

    @classmethod
    def search(cls, **attrs):
        rept_event_qs = cls.query().filter(**attrs)
        return rept_event_qs
