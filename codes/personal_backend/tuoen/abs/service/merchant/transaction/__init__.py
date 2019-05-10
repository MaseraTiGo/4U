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

from model.store.model_merchant_transaction import MerchantTransaction
from model.store.model_product import Product



class MerchantTransactionHelper(object):

    @classmethod
    def generate(cls, **attrs):
        """添加商户流水"""
        merchant_transaction = MerchantTransaction.create(**attrs)
        if merchant_transaction is None:
            raise BusinessError("商户流水添加失败")
        return merchant_transaction

    @classmethod
    def search(cls, **search_info):
        """商户流水搜索"""
        merchant_transaction_qs = MerchantTransaction.search(**search_info)
        return merchant_transaction_qs

    @classmethod
    def is_exit(cls, **check_info):
        """商户流水是否存在"""
        merchant_transaction_qs = cls.search(**check_info)
        if merchant_transaction_qs.count() > 0:
            return True
        return False

    @classmethod
    def sum_amount_bymerchant(cls, merchant):
        """根据商户求流水和"""
        merchant_transaction_qs = MerchantTransaction.search(merchant = merchant)
        sum_result = merchant_transaction_qs.aggregate(sum_amount = Sum('tx_amt'))
        sum_amount = sum_result["sum_amount"]
        return sum_amount

    @classmethod
    def check_is_activation(cls, merchant):
        """判断流水是否达到某个值"""
        sum_amount = cls.sum_amount_bymerchant(merchant)
        product_qs = Product.search(name = "银收宝")
        rebate_money = 0
        if product_qs.count() > 0:
            rebate_money = product_qs[0].rebate_money
        if sum_amount > rebate_money:
            return True
        return False
