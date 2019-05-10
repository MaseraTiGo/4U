# coding=UTF-8

'''
Created on 2016年7月22日

@author: Administrator
'''

from django.db.models import *
from django.utils import timezone
from model.base import BaseModel


class Product(BaseModel):
    name = CharField(verbose_name="商品名称", max_length=64, default="")
    alias = CharField(verbose_name="商品别名", max_length=64, default="")
    introduction = TextField(verbose_name="商品简介")
    details = TextField(verbose_name="商品详情")
    thumbnail = CharField(verbose_name="商品缩略图", max_length=256, default="")
    images = TextField(verbose_name="商品banner图")
    postage = IntegerField(verbose_name="商品邮费/分", default=0)
    rebate_money = IntegerField(verbose_name="返利金额/分", default=0)
    p_type = CharField(verbose_name="类型", max_length=64, default="")
    code = CharField(verbose_name="编号", max_length=64, default="")
    provider = CharField(verbose_name="供应商", max_length=64, default="")
    update_time = DateTimeField(verbose_name="更新时间", auto_now=True)
    create_time = DateTimeField(verbose_name="创建时间", default=timezone.now)

    @classmethod
    def search(cls, **attrs):
        product_qs = cls.query().filter(**attrs)
        return product_qs


class ProductModel(BaseModel):
    product = ForeignKey(Product, on_delete=CASCADE)
    name = CharField(verbose_name="型号名称", max_length=64, default="")
    rate = CharField(verbose_name="默认费率表", max_length=128, default=100)
    remark = TextField(verbose_name="备注", default="")
    stock = IntegerField(verbose_name="商品库存", default=0)

    update_time = DateTimeField(verbose_name="更新时间", auto_now=True)
    create_time = DateTimeField(verbose_name="创建时间", default=timezone.now)

    @classmethod
    def search(cls, **attrs):
        product__model_qs = cls.query().filter(**attrs)
        return product__model_qs
