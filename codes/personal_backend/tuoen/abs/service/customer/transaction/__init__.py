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

from model.models import EquipmentTransaction


class TransactionServer(object):

    @classmethod
    def search(cls, current_page, **search_info):
        """查询交易流水列表"""
        transaction_qs = cls.search_qs(**search_info)
        transaction_qs = transaction_qs.order_by("-id")

        return Splitor(current_page, transaction_qs)

    @classmethod
    def search_qs(cls, **search_info):
        """查询交易流水列表"""
        transaction_qs = EquipmentTransaction.search(**search_info)

        return transaction_qs

    @classmethod
    def hung_transaction_forregister(cls, customer_register_list, **search_info):
        """挂载交易流水"""

        customer_register_mapping = {}
        for customer_register in customer_register_list:
            customer_register_mapping[customer_register.id] = customer_register
            customer_register.transaction_list = []

        search_info.update({"code_id__in":customer_register_mapping.keys()})
        transaction_qs = cls.search_qs(**search_info)
        for transaction in transaction_qs:
            if transaction.code_id in customer_register_mapping:
                # customer_register_mapping[transaction.code_id].transaction_list.append(transaction)
                transaction.device_code = customer_register_mapping[transaction.code_id].device_code

        return transaction_qs

