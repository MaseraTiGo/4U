# coding=UTF-8

'''
Created on 2016年7月22日

@author: Administrator
'''

import hashlib
import datetime
import json
import random

from tuoen.sys.core.exception.business_error import BusinessError
from tuoen.sys.utils.common.split_page import Splitor

from model.models import Customer

from tuoen.abs.service.customer.salechance import SaleChanceHelper
from tuoen.abs.service.customer.register import CustomerRegisterHelper

class CustomerServer(object):

    @classmethod
    def search(cls, current_page, **search_info):
        """查询客户列表"""

        customer_qs = cls.search_qs(**search_info)

        return Splitor(current_page, customer_qs)

    @classmethod
    def get(cls, customer_id):
        """查询客户详情"""

        customer = Customer.get_byid(customer_id)
        if customer is None:
            raise BusinessError("客户不存在")
        return customer

    @classmethod
    def update(cls, customer, **attr):
        """修改客户信息"""

        customer.update(**attr)
        return customer

    @classmethod
    def search_qs(cls, **search_info):
        """查询客户列表"""

        customer_qs = Customer.search(**search_info)
        customer_qs.order_by("-create_time")
        return customer_qs


    @classmethod
    def hung_device_code(cls, service_item_list):
        customer_mapping = {}
        customer_ids = []
        for service_item in service_item_list:
            if service_item.customer_id:
                customer_ids.append(service_item.customer_id)

        customer_list = cls.search_qs(id__in = customer_ids)
        for customer in customer_list:
            customer_mapping[customer.id] = customer

        for service_item in service_item_list:
            service_item.phone_code = ""
            if service_item.customer_id:
                cus = customer_mapping.get(service_item.customer_id)
                #  when 'cus' is None, exception occurred, so, there needs pre-check ---20180726
                if cus:
                    if cus.mobiledevices:
                        service_item.phone_code = cus.mobiledevices.code

        return service_item_list

class SaleChanceServer(object):

    @classmethod
    def generate(cls, **attr):
        """生成销售机会列表"""

        return SaleChanceHelper.generate(**attr)

    @classmethod
    def search(cls, current_page, **search_info):
        """查询销售机会列表"""

        return SaleChanceHelper.search(current_page, **search_info)

    @classmethod
    def update(cls, sale_chance_id, **attrs):
        """更新销售机会列表"""

        return SaleChanceHelper.update(sale_chance_id, **attrs)

    @classmethod
    def get(cls, sale_chance_id):
        """获取销售机会详情"""

        return SaleChanceHelper.get(sale_chance_id)

class CustomerRegisterServer(object):
    @classmethod
    def search(cls, current_page, **search_info):
        """查询客戶註冊列表"""
        return CustomerRegisterHelper.search(current_page, **search_info)

    @classmethod
    def search_all(cls, **search_info):
        """查询所有客戶注册列表"""
        return CustomerRegisterHelper.search_all(**search_info)
