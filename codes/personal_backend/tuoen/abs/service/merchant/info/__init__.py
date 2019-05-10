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

from model.store.model_merchant import Merchant


class MerchantHelper(object):

    @classmethod
    def generate(cls, **attrs):
        """添加商户"""
        merchant = Merchant.create(**attrs)
        if merchant is None:
            raise BusinessError("商户添加失败")
        return merchant

    @classmethod
    def search(cls, current_page, **search_info):
        """查询商户列表-分页"""
        merchant_qs = cls.search_qs(**search_info)
        merchant_qs = merchant_qs.order_by("-create_time")
        return Splitor(current_page, merchant_qs)

    @classmethod
    def search_qs(cls, **search_info):
        """查询商户列表"""
        return Merchant.search(**search_info)

    @classmethod
    def get_merchant_bymid(cls, merchant_id):
        """根据商户编号查询商户"""
        merchant = None
        merchant_qs = cls.search_qs(merchant_id = merchant_id)
        if merchant_qs.count() > 0:
            merchant = merchant_qs[0]
        return merchant

