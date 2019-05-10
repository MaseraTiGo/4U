# coding=UTF-8

'''
Created on 2016年7月22日

@author: Administrator
'''

from django.db.models import *
from model.base import BaseModel
from model.store.model_user import Staff
from model.store.model_shop import Shop

class MeasureShop(BaseModel):
    """店铺绩效"""
    staff = ForeignKey(Staff, on_delete=CASCADE)
    shop = ForeignKey(Shop, on_delete=CASCADE)

    total_sales = IntegerField(verbose_name = "销售总数", default = 0)
    add_order_number = IntegerField(verbose_name = "补单数量", default = 0)

    add_order_per_money = IntegerField(verbose_name = "单次补单金额/分", default = 0)
    add_order_total_money = IntegerField(verbose_name = "补单费用", default = 0)

    single_point_per_money = IntegerField(verbose_name = "单次扣点金额/分", default = 0)
    single_point_total_money = IntegerField(verbose_name = "扣点费用/分", default = 0)

    through_number = IntegerField(verbose_name = "直通车成交单数", default = 0)
    through_money = IntegerField(verbose_name = "直通车总花费/分", default = 0)

    freight = IntegerField(verbose_name = "运费单价/分", default = 0)
    total_freight = IntegerField(verbose_name = "总运费/分", default = 0)

    record_date = DateField(verbose_name = "报表日期", max_length = 20, null = True, blank = True)

    remark = TextField(verbose_name = "备注")

    update_time = DateTimeField(verbose_name = "更新时间", auto_now = True)
    create_time = DateTimeField(verbose_name = "创建时间", auto_now_add = True)

    @classmethod
    def search(cls, **attrs):
        measure_shop_qs = cls.query().filter(**attrs)
        return measure_shop_qs
