# coding=UTF-8

'''
Created on 2016年7月22日

@author: Administrator
'''

from django.db.models import *
from django.utils import timezone
from model.base import BaseModel
from model.store.model_customer import Customer
from model.store.model_shop import Shop, Goods
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


class Order(BaseModel):
    shop = ForeignKey(Shop, on_delete=CASCADE)
    customer = ForeignKey(Customer, on_delete=CASCADE)

    order_sn = CharField(verbose_name = "订单编号", max_length = 128, default = "")
    paytype = CharField(verbose_name = "支付类型", max_length = 64, choices = PayTypes.CHOICES, default = PayTypes.OTHER)
    total_price = IntegerField(verbose_name = "订单价格/分", default = 0)
    total_quantity = IntegerField(verbose_name = "总数量")
    pay_time = DateTimeField(verbose_name = "支付时间", max_length = 20, null = True, blank = True, db_index = True)
    status = CharField(verbose_name = "支付状态", max_length = 64, choices = StatusTypes.CHOICES, default = StatusTypes.SUBMIT)
    transaction_id = CharField(verbose_name = "第三方支付id", max_length = 128, default = "")
    consignee = CharField(verbose_name = "收货人", max_length = 32, default = "", null = True)
    city = CharField(verbose_name = "城市", max_length = 128, default = "", null = True)
    address = CharField(verbose_name = "详细地址", max_length = 128, default = "", null = True)
    phone = CharField(verbose_name = "收货人电话", max_length = 128, default = "", null = True)
    messages = TextField(verbose_name = "买家留言")
    remark = TextField(verbose_name = "备注", default = "" , null = True)

    update_time = DateTimeField(verbose_name = "更新时间", auto_now = True)
    create_time = DateTimeField(verbose_name = "创建时间", default = timezone.now)

    @classmethod
    def search(cls, **attrs):
        order_qs = cls.query().filter(**attrs)
        return order_qs

class OrderItem(BaseModel):
    order = ForeignKey(Order, on_delete=CASCADE)
    # goods_id = IntegerField(verbose_name = "商品id", default = 0)
    goods = ForeignKey(Goods, null = True, on_delete=CASCADE)

    name = CharField(verbose_name = "商品名称", max_length = 64, default = "")
    alias = CharField(verbose_name = "商品别名", max_length = 64, default = "")
    code = CharField(verbose_name = "商品编码", max_length = 64, default = "")
    price = IntegerField(verbose_name = "商品价格", default = 0)
    rate = CharField(verbose_name = "商品费率", max_length = 64, default = "")
    introduction = TextField(verbose_name = "商品简介")
    thumbnail = CharField(verbose_name = "商品缩略图", max_length = 256, default = "")
    postage = IntegerField(verbose_name = "商品邮费", default = 0)
    type = CharField(verbose_name = "商品类型", max_length = 64, default = "")

    quantity = IntegerField(verbose_name = "购买数量", default = 0)

    update_time = DateTimeField(verbose_name = "更新时间", auto_now = True)
    create_time = DateTimeField(verbose_name = "创建时间", default = timezone.now)

    @classmethod
    def search(cls, **attrs):
        order_item_qs = cls.query().filter(**attrs)
        return order_item_qs
