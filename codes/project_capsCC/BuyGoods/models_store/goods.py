# -*- coding: utf-8 -*-
# file_name       : goods.py
# file_func       :
# file_author     : 'Johnathan.Wick'
# file_create_date: 2019/9/27 15:37

from django.db import models
from BuyGoods.models_store import BaseModel


class Keywords(BaseModel):
    word = models.CharField(max_length=64, default='your name is the most lovely letter')

    class Meta:
        db_table = 'keywords'

    @property
    def goods_list(self):
        return (good for good in self.goods_kw.all())

    @property
    def shops_list(self):
        return (shop for shop in self.shop_kw.all())


class Goods(BaseModel):
    name = models.CharField(max_length=128, default='Unsolved')
    price = models.FloatField(default=0.0)
    sales = models.BigIntegerField(default=0)
    score = models.FloatField(default=0.0)
    brief = models.CharField(max_length=256, default='the guy is so lazy, nothing left')
    keywords = models.ManyToManyField('Keywords', related_name='goods_kw', related_query_name='goods_kw_q')
    shop = models.ManyToManyField('Shop', related_name='goods_shop', related_query_name='goods_shop_q')

    class Meta:
        db_table = 'goods'

    @property
    def keywords_list(self):
        return [obj.word for obj in self.keywords.all()]

    @property
    def shop_list(self):
        return [shop for shop in self.shop.all()]


class Shop(BaseModel):
    name = name = models.CharField(max_length=128, default='Unsolved')
    score = models.FloatField(default=0.0)
    brief = models.CharField(max_length=256, default='the guy is so lazy, nothing left')
    keywords = models.ManyToManyField(Keywords, related_name='shop_kw', related_query_name='shop_kw_q')

    class Meta:
        db_table = 'shop'

    @property
    def goods_list(self):
        return (good for good in self.goods_set.all())

    @property
    def keywords_list(self):
        return [kw.word for kw in self.keywords.all()]
