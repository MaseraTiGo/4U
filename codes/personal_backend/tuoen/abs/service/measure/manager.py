# coding=UTF-8

'''
Created on 2016年7月22日

@author: Administrator
'''

import hashlib
import datetime
import time
import json
import random

from tuoen.sys.core.exception.business_error import BusinessError
from tuoen.sys.utils.common.split_page import Splitor
from tuoen.sys.utils.common.dictwrapper import DictWrapper

from tuoen.abs.service.measure.shop import MeasureShopHelper
from tuoen.abs.service.measure.staff import MeasureStaffHelper


class MeasureShopServer(object):

    @classmethod
    def generate(cls, **report_info):
        """创建店铺绩效"""

        report = MeasureShopHelper.generate(**report_info)

        return report

    @classmethod
    def search(cls, current_page, search_qs):
        """查询店铺绩效列表"""

        page_list = MeasureShopHelper.search(current_page, search_qs)

        return page_list

    @classmethod
    def search_qs(cls, **search_info):
        """查询店铺绩效列表"""

        search_qs = MeasureShopHelper.search_qs(**search_info)

        return search_qs

    @classmethod
    def get(cls, report_id):
        """获取店铺绩效详情"""

        report = MeasureShopHelper.get(report_id)

        return report

    @classmethod
    def update(cls, measure_shop, **attrs):
        """编辑店铺绩效"""

        MeasureShopHelper.update(measure_shop, **attrs)

        return True

    @classmethod
    def remove(cls, report_id):
        """移除店铺绩效"""

        MeasureShopHelper.remove(report_id)

        return True

    @classmethod
    def check_repeat(cls, measure_shop=None, **check_info):
        return MeasureShopHelper.check_repeat(measure_shop, **check_info)

    @classmethod
    def hung_measure_forshops(cls, shop_list):
        """挂载店铺绩效"""
        MeasureShopHelper.hung_measure_forshops(shop_list)

        shop_mapping = {}
        measure_shop = []
        for shop in shop_list:
            for key in shop.measure_shop:
                shop.measure_shop[key].shop = shop
                cls.calculation_byitem(shop.measure_shop[key])

        return shop_list

    @classmethod
    def calculation(cls, measure_shop_list):
        """"计算店铺绩效"""

        for measure_shop in measure_shop_list:
            cls.calculation_byitem(measure_shop)
        return measure_shop_list

    @classmethod
    def calculation_byitem(cls, measure_shop):
        """"计算店铺绩效"""
        measure_shop.total_spend = measure_shop.add_order_total_money + measure_shop.single_point_total_money + \
                                   measure_shop.total_freight + measure_shop.through_money
        if measure_shop.total_sales > 0:
            measure_shop.average_spend = int(round(measure_shop.total_spend / measure_shop.total_sales))
        else:
            measure_shop.average_spend = 0

        return measure_shop

    @classmethod
    def summing_new(cls, **search_info):
        sum_data = MeasureShopHelper.summing_new(**search_info)
        sum_data = cls.calculation_byitem(sum_data)
        return sum_data;

    @classmethod
    def summing(cls, measure_shop_qs):
        total_sales_sum_list = []
        add_order_number_sum_list = []
        add_order_total_money_sum_list = []
        single_point_total_money_sum_list = []
        through_number_sum_list = []
        through_money_sum_list = []
        total_freight_sum_list = []

        sum_data = DictWrapper({})

        for measure_shop in measure_shop_qs:
            total_sales_sum_list.append(measure_shop.total_sales)
            add_order_number_sum_list.append(measure_shop.add_order_number)
            add_order_total_money_sum_list.append(measure_shop.add_order_total_money)
            single_point_total_money_sum_list.append(measure_shop.single_point_total_money)
            through_number_sum_list.append(measure_shop.through_number)
            through_money_sum_list.append(measure_shop.through_money)
            total_freight_sum_list.append(measure_shop.total_freight)

        sum_data.total_sales = sum(total_sales_sum_list)
        sum_data.add_order_number = sum(add_order_number_sum_list)
        sum_data.add_order_total_money = sum(add_order_total_money_sum_list)
        sum_data.single_point_total_money = sum(single_point_total_money_sum_list)
        sum_data.through_number = sum(through_number_sum_list)
        sum_data.through_money = sum(through_money_sum_list)
        sum_data.total_freight = sum(total_freight_sum_list)

        sum_data = cls.calculation_byitem(sum_data)

        return sum_data;


class MeasureStaffServer(object):

    @classmethod
    def generate(cls, **report_info):
        """创建员工绩效"""

        measure_staff = MeasureStaffHelper.generate(**report_info)

        return measure_staff

    @classmethod
    def search(cls, current_page, search_qs):
        """查询员工绩效列表"""

        page_list = MeasureStaffHelper.search(current_page, search_qs)

        return page_list

    @classmethod
    def search_qs(cls, **search_info):
        search_qs = MeasureStaffHelper.search_qs(**search_info)
        return search_qs

    @classmethod
    def check_repeat(cls, measure_staff=None, **check_info):
        return MeasureStaffHelper.check_repeat(measure_staff, **check_info)

    @classmethod
    def get(cls, measure_staff_id):
        """获取员工绩效详情"""

        report = MeasureStaffHelper.get(measure_staff_id)

        return report

    @classmethod
    def update(cls, measure_staff, **attrs):
        """编辑员工绩效"""

        MeasureStaffHelper.update(measure_staff, **attrs)

        return True

    @classmethod
    def remove(cls, measure_staff_id):
        """移除员工绩效"""

        MeasureStaffHelper.remove(measure_staff_id)

        return True

    @classmethod
    def calculation(cls, measure_staff_list):

        for measure_staff in measure_staff_list:
            if measure_staff.exhale_number > 0:
                measure_staff.call_rate = "{rate}%".format(
                    rate=str(round((measure_staff.call_number / measure_staff.exhale_number * 100), 2)))
            else:
                measure_staff.call_rate = "0"

        return measure_staff_list

    @classmethod
    def summing_new(self, **search_info):
        return MeasureStaffHelper.summing_new(**search_info)

    @classmethod
    def summing(cls, measure_staff_qs):
        new_number_sum_list = []
        exhale_number_sum_list = []
        call_number_sum_list = []
        wechat_number_sum_list = []

        sum_data = DictWrapper({})

        for measure_staff in measure_staff_qs:
            new_number_sum_list.append(measure_staff.new_number)
            exhale_number_sum_list.append(measure_staff.exhale_number)
            call_number_sum_list.append(measure_staff.call_number)
            wechat_number_sum_list.append(measure_staff.wechat_number)

        sum_data.new_number = sum(new_number_sum_list)
        sum_data.exhale_number = sum(exhale_number_sum_list)
        sum_data.call_number = sum(call_number_sum_list)
        sum_data.wechat_number = sum(wechat_number_sum_list)
        sum_data.call_rate = "0%"

        if sum_data.exhale_number > 0:
            sum_data.call_rate = "{rate}%".format(
                rate=str(round((sum_data.call_number / sum_data.exhale_number * 100), 2)))
        return sum_data;

    @classmethod
    def Statistics(cls, search_time=None):
        if isinstance(search_time, dict):
            search_time_in = search_time['search_time']
            user_pro = search_time['cur_user']
        if search_time_in is None:
            current_time = datetime.datetime.now()
        else:
            current_time = search_time_in
        cur_date_first = datetime.date(current_time.year, current_time.month, 1)
        cur_date_last = datetime.date(current_time.year, current_time.month + 1, 1) - datetime.timedelta(1)
        if user_pro:
            measure_staff_list = MeasureStaffHelper.search_qs(begin_time=cur_date_first, end_time=cur_date_last,
                                                              cur_user=user_pro)
        else:
            measure_staff_list = MeasureStaffHelper.search_qs(begin_time=cur_date_first, end_time=cur_date_last)
        measure_staff_mapping = {}
        cal_time = cur_date_last
        while (cal_time >= cur_date_first):
            temp_calc = DictWrapper({
            })

            temp_calc.new_number = 0
            temp_calc.exhale_number = 0
            temp_calc.call_number = 0
            temp_calc.call_rate = '0%'
            temp_calc.wechat_number = 0
            temp_calc.volume = 0
            temp_calc.conversion_rate = '0%'
            temp_calc.open_number = 0
            temp_calc.open_rate = '0%'
            temp_calc.activation_number = 0
            temp_calc.activation_rate = '0%'

            temp_calc_day = {}
            time_str = cal_time.strftime('%Y-%m-%d')
            measure_staff_mapping[time_str] = temp_calc
            cal_time = cal_time - datetime.timedelta(1)
        for measure_staff in measure_staff_list:
            report_date_str = str(measure_staff.report_date)
            temp_item = measure_staff_mapping[report_date_str]
            temp_item["new_number"] += measure_staff.new_number
            temp_item["exhale_number"] += measure_staff.exhale_number
            temp_item["call_number"] += measure_staff.call_number
            temp_item["wechat_number"] += measure_staff.wechat_number
        return measure_staff_mapping

    @classmethod
    def staff_sum_list(cls, current_page, is_split=True, **search_info):
        return MeasureStaffHelper.staff_sum_list(current_page, is_split=is_split, **search_info)

    @classmethod
    def total_calculate(cls, **search_info):
        return MeasureStaffHelper.total_calculate(**search_info)

    @classmethod
    def hung_total_rate(cls, sum_data, **search_info):
        return MeasureStaffHelper.hung_total_rate(sum_data, **search_info)

    @classmethod
    def hung_ysb_total_rate(cls, sum_data, **search_info):
        return MeasureStaffHelper.hung_ysb_total_rate(sum_data, **search_info)

    @classmethod
    def hung_ysb_measure_data(cls, staff_obj, date_min, date_max):
        MeasureStaffHelper.hung_ysb_measure_data(staff_obj, date_min, date_max)
