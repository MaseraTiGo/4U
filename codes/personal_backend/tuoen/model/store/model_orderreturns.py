# coding=UTF-8

'''
Created on 2016年7月22日

@author: Administrator
'''

from django.db.models import *
from django.utils import timezone
from model.base import BaseModel
from model.store.model_order import Order
from model.models import Staff
from model.store.model_customer import Customer

class PayTypes(object):
    WECHAT = "wechat"
    ALIPAY = "alipay"
    OTHER = "other"
    CHOICES = ((WECHAT, '微信'), (ALIPAY, "支付宝"), (OTHER, "其他"))


class StatusTypes(object):
    UNPAID = "unpaid"
    SUBMIT = "submit"
    PAYED = "payed"
    SENDED = "sended"
    FINISHED = "finished"
    CHOICES = ((UNPAID, '未支付'), (SUBMIT, '已下单'), (PAYED, "已支付"), (SENDED, "已发货"), (FINISHED, "已发货"))

class ReturnsNum(object):
    @property
    def returns_num(self):
        import time
        import random
        prefix = 'TH'
        rand_num = str(random.randint(1000, 9999))
        time_mark = str(int(time.time()))
        returns_num = prefix + time_mark + rand_num
        return returns_num

class OrderReturns(BaseModel):
    order = ForeignKey(Order, null = True, on_delete=CASCADE)
    code = CharField(verbose_name = "设备编码", max_length = 128, default = "")
    returns_num = CharField(verbose_name="退貨單號", max_length=128, default="")
    last_cal_time = DateTimeField(verbose_name = "最后统计时间", max_length = 20, null = True, blank = True)
    total_amount = IntegerField(verbose_name = "交易总额/分", default = 0)
    buyinfo_status = CharField(verbose_name="购买信息状态", max_length=64, default='red')
    dsinfo_status = CharField(verbose_name="电刷信息状态", max_length=64, default='red')
    rebate_status = CharField(verbose_name="激活信息状态", max_length=64, default='red')
    sn_status = CharField(verbose_name="设备码出入库状态", max_length=64, default='red')
    remark = CharField(verbose_name = "備註", max_length = 128, default = "")
    update_time = DateTimeField(verbose_name = "更新时间", auto_now = True)
    create_time = DateTimeField(verbose_name = "创建时间", default = timezone.now)

    @classmethod
    def search(cls, **attrs):
        order_returns_qs = cls.query().filter(**attrs)
        return order_returns_qs

