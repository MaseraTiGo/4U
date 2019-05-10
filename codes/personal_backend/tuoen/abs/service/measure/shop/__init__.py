# coding=UTF-8

'''
Created on 2016年7月22日

@author: Administrator
'''

import hashlib
import datetime
import json
import random

from django.db.models import *

from tuoen.sys.core.exception.business_error import BusinessError
from tuoen.sys.utils.common.split_page import Splitor
from tuoen.sys.utils.common.dictwrapper import DictWrapper

from model.models import MeasureShop


class MeasureShopHelper(object):

    @classmethod
    def calculation(cls, **report_info):
        shop = report_info["shop"]
        add_order_total_money = report_info["add_order_number"] * shop.single_repair_money
        single_point_total_money = (report_info["total_sales"] + report_info["add_order_number"]) * shop.single_point_money
        total_freight = report_info["total_sales"] * shop.freight
        report_info.update({"add_order_per_money":shop.single_repair_money})
        report_info.update({"add_order_total_money":add_order_total_money})
        report_info.update({"single_point_per_money":shop.single_point_money})
        report_info.update({"single_point_total_money":single_point_total_money})
        report_info.update({"freight":shop.freight})
        report_info.update({"total_freight":total_freight})

        return report_info


    @classmethod
    def generate(cls, **report_info):
        """创建店铺绩效"""

        report_info = cls.calculation(**report_info)

        report = MeasureShop.create(**report_info)
        if report is None:
            raise BusinessError("店铺绩效添加失败")

        return report

    @classmethod
    def search(cls, current_page, report_qs):
        """查询店铺绩效列表"""

        report_qs = report_qs.order_by("-record_date")
        return Splitor(current_page, report_qs)

    @classmethod
    def search_qs(cls, **search_info):
        """查询店铺绩效列表"""
        if "begin_time" in search_info:
            begin_time = search_info.pop("begin_time")
            search_info.update({"record_date__gte":begin_time})
        if "end_time" in search_info:
            end_time = search_info.pop("end_time")
            search_info.update({"record_date__lte":end_time})
        report_qs = MeasureShop.search(**search_info).order_by("-record_date")
        return report_qs

    @classmethod
    def get(cls, report_id):
        """获取店铺绩效详情"""

        report = MeasureShop.get_byid(report_id)
        if report is None:
            raise BusinessError("店铺绩效不存在")
        return report

    @classmethod
    def check_repeat(cls, measure_shop = None, **check_info):
        measure_shop_qs = cls.search_qs(**check_info)
        if measure_shop is not None:
            measure_shop_qs = measure_shop_qs.filter(~Q(id = measure_shop.id))
        if measure_shop_qs.count() > 0:
            raise BusinessError("请不要添加重复绩效")
        return True

    @classmethod
    def update(cls, measure_shop, **attrs):
        """编辑店铺绩效"""

        attrs = cls.calculation(**attrs)
        measure_shop.update(**attrs)
        return True

    @classmethod
    def remove(cls, report_id):
        """移除店铺绩效"""

        report = cls.get(report_id)
        report.delete()

        return True

    @classmethod
    def summing_new(cls, **search_info):
        sum_data = DictWrapper({})
        measure_shop_qs = cls.search_qs(**search_info)
        measure_shop_result = measure_shop_qs.aggregate(sum_sales = Sum('total_sales'), \
                                                      sum_order_number = Sum('add_order_number'), \
                                                      sum_order_total_money = Sum('add_order_total_money'), \
                                                      sum_point_total_money = Sum('single_point_total_money'), \
                                                      sum_through_number = Sum('through_number'), \
                                                      sum_through_money = Sum('through_money'), \
                                                      sum_total_freight = Sum('total_freight'))
        sum_data.total_sales = measure_shop_result["sum_sales"] if measure_shop_result["sum_sales"] else 0
        sum_data.add_order_number = measure_shop_result["sum_order_number"] if measure_shop_result["sum_order_number"] else 0
        sum_data.add_order_total_money = measure_shop_result["sum_order_total_money"] if measure_shop_result["sum_order_total_money"] else 0
        sum_data.single_point_total_money = measure_shop_result["sum_point_total_money"] if measure_shop_result["sum_point_total_money"] else 0
        sum_data.through_number = measure_shop_result["sum_through_number"] if measure_shop_result["sum_through_number"] else 0
        sum_data.through_money = measure_shop_result["sum_through_money"] if measure_shop_result["sum_through_money"] else 0
        sum_data.total_freight = measure_shop_result["sum_total_freight"] if measure_shop_result["sum_total_freight"] else 0
        return sum_data

    @classmethod
    def hung_measure_forshops(cls, shop_list):
        """店铺挂载店铺绩效"""
        current_time = datetime.datetime.now()
        day_begin = '%d-%02d-01' % (current_time.year, current_time.month)
        day_begin = datetime.datetime.strptime("2018-05-01", '%Y-%m-%d')
        day_end = datetime.datetime.strptime("2018-06-01", '%Y-%m-%d')

        measure_shop_qs = MeasureShop.search(record_date__range = (day_begin, day_end))

        chance_time = day_begin
        init_data = {}
        while(chance_time < current_time):
            init_data[chance_time.strftime('%Y-%m-%d')] = DictWrapper({})
            init_data_item = init_data[chance_time.strftime('%Y-%m-%d')]
            init_data_item.total_sales = 0
            init_data_item.add_order_number = 0
            init_data_item.through_number = 0
            init_data_item.through_money = 0
            init_data_item.shop = None
            chance_time = chance_time + datetime.timedelta(days = 1)

        shop_mapping = {}
        for shop in shop_list:
            shop.measure_shop = init_data
            shop_mapping[shop.id] = shop

        last_day = day_begin + datetime.timedelta(days = -1)

        measure_shop_qs = measure_shop_qs.values('shop_id', 'record_date').\
            annotate(count = Count('record_date'), sum_total_sales = Sum('total_sales'), sum_add_order_number = Sum('add_order_number'), \
                      sum_through_number = Sum('through_number'), sum_through_money = Sum('through_money'))

        for measure_shop_item in measure_shop_qs:
            if measure_shop_item["shop_id"] in shop_mapping:
                shop_month_date_item = shop_mapping[measure_shop_item["shop_id"]].measure_shop[measure_shop_item["record_date"].strftime('%Y-%m-%d')]
                shop_month_date_item.total_sales = measure_shop_item["sum_total_sales"]
                shop_month_date_item.add_order_number = measure_shop_item["sum_add_order_number"]
                shop_month_date_item.through_number = measure_shop_item["sum_through_number"]
                shop_month_date_item.through_money = measure_shop_item["sum_through_money"]

        return shop_list
