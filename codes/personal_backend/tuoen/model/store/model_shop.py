# coding=UTF-8

'''
Created on 2016年7月22日

@author: Administrator
'''

from django.db.models import *
from django.utils import timezone
from model.base import BaseModel
from model.store.model_product import ProductModel


class Channel(BaseModel):
    name = CharField(verbose_name="名称", max_length=64, default="")
    freight = IntegerField(verbose_name="运费/分", default=0)
    single_repair_money = IntegerField(verbose_name="单次补单金额/分", default=0)
    single_point_money = IntegerField(verbose_name="单次扣点金额/分", default=0)
    remark = TextField(verbose_name="备注")

    update_time = DateTimeField(verbose_name="更新时间", auto_now=True)
    create_time = DateTimeField(verbose_name="创建时间", default=timezone.now)

    @classmethod
    def search(cls, **attrs):
        channel_qs = cls.query().filter(**attrs)
        return channel_qs


class Shop(BaseModel):
    channel = ForeignKey(Channel, null=True, on_delete=CASCADE)
    name = CharField(verbose_name="店铺名称", max_length=64, default="")
    freight = IntegerField(verbose_name="运费/分", default=0)
    single_repair_money = IntegerField(verbose_name="单次补单金额/分", default=0)
    single_point_money = IntegerField(verbose_name="单次扣点金额/分", default=0)
    is_distribution = BooleanField(verbose_name="是否为分销店铺", default=False)
    remark = TextField(verbose_name="备注")

    update_time = DateTimeField(verbose_name="更新时间", auto_now=True)
    create_time = DateTimeField(verbose_name="创建时间", default=timezone.now)

    @classmethod
    def get_shop_buyname(cls, name):
        """根据名称查询店铺"""
        try:
            return cls.query().filter(name=name)[0]
        except:
            return None

    @classmethod
    def search(cls, **attrs):
        shop_qs = cls.query().filter(**attrs)
        return shop_qs


class Goods(BaseModel):
    shop = ForeignKey(Shop, null=True, on_delete=CASCADE)
    # product_id = IntegerField(verbose_name = "产品id", default = 0)
    # product_model_id = IntegerField(verbose_name = "产品id", default = 0)
    product_model = ForeignKey(ProductModel, null=True, on_delete=CASCADE)
    name = CharField(verbose_name="商品名称", max_length=64, default="")
    alias = CharField(verbose_name="商品别名", max_length=64, default="")
    code = CharField(verbose_name="商品编码", max_length=64, default="")
    price = IntegerField(verbose_name="商品价格/分", default=0)
    rate = CharField(verbose_name="商品费率", max_length=64, default="")
    introduction = TextField(verbose_name="商品简介")
    details = TextField(verbose_name="商品详情")
    thumbnail = CharField(verbose_name="商品缩略图", max_length=256, default="")
    images = TextField(verbose_name="商品banner图")
    postage = IntegerField(verbose_name="商品邮费/分", default=0)
    re_num = IntegerField(verbose_name="商品限购数量", default=0)

    create_time = DateTimeField(verbose_name="创建时间", default=timezone.now)
    update_time = DateTimeField(verbose_name="更新时间", auto_now=True)
