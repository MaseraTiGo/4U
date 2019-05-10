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

from tuoen.abs.service.merchant.info import MerchantHelper
from tuoen.abs.service.merchant.equipment import MerchantEquipmentHelper
from tuoen.abs.service.merchant.transaction import MerchantTransactionHelper


class MerchantServer(object):

    @classmethod
    def generate(cls, **attrs):
        """添加商户"""
        return MerchantHelper.generate(**attrs)

    @classmethod
    def search(cls, current_page, **search_info):
        """查询商户列表-分页"""
        return MerchantHelper.search(current_page, **search_info)

    @classmethod
    def search_qs(cls, **search_info):
        """查询商户列表"""
        return MerchantHelper.search_qs(**search_info)

    @classmethod
    def get_merchant_bymid(cls, merchant_id):
        """根据商户编号查询商户"""
        return MerchantHelper.get_merchant_bymid(merchant_id)


class MerchantEquipmentServer(object):

    @classmethod
    def generate(cls, **attrs):
        """添加商户设备关系"""
        return MerchantEquipmentHelper.generate(**attrs)

    @classmethod
    def batch_generate(cls, merchant_equipment_list):
        """批量添加商户设备关系表"""
        return MerchantEquipmentHelper.batch_generate(merchant_equipment_list)


class MerchantTransactionServer(object):

    @classmethod
    def generate(cls, **attrs):
        """添加商户流水"""
        return MerchantTransactionHelper.generate(**attrs)

    @classmethod
    def search(cls, **search_info):
        """商户流水搜索"""
        return MerchantTransactionHelper.search(**search_info)

    @classmethod
    def is_exit(cls, **check_info):
        """商户流水是否存在"""
        return MerchantTransactionHelper.search(**check_info)

    @classmethod
    def check_is_activation(cls, merchant):
        """判断流水是否达到某个值"""
        return MerchantTransactionHelper.check_is_activation(merchant)
