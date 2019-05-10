# coding=UTF-8

'''
Created on 2016年7月22日

@author: Administrator
'''

from django.db.models import *
from django.utils import timezone
from model.base import BaseModel
from model.store.model_merchant import Merchant


class TransactionStatus(object):
    SUCCESS = "success"
    FAIL = "fail"
    CHOICES = ((SUCCESS, '交易成功'), (FAIL, "交易失败"))


class MerchantTransaction(BaseModel):
    """商户流水表"""
    merchant = ForeignKey(Merchant, on_delete=CASCADE)
    merchant_sn = CharField(verbose_name = "商户编号", max_length = 256, default = "")
    organ_id = CharField(verbose_name = "机构编号（代理商编号）", max_length = 256, default = "")
    serial_no = CharField(verbose_name = "设备硬件系列号", max_length = 256, default = "")
    terminal_id = CharField(verbose_name = "终端编号", max_length = 256, default = "")
    trans_id = CharField(verbose_name = "交易编号", max_length = 256, default = "")
    trans_type = IntegerField(verbose_name = "交易类型", default = 0)
    tx_date = DateTimeField(verbose_name = "交易时间", null = True, blank = True)
    tx_amt = IntegerField(verbose_name = "交易金额/分", default = 0)
    act_amt = IntegerField(verbose_name = "实际到账金额/分", default = 0)
    tx_ref_id = CharField(verbose_name = "交易参考号", max_length = 256, default = "")
    order_no = CharField(verbose_name = "订单号", max_length = 256, default = "")
    pid = CharField(verbose_name = "产品编号", max_length = 256, default = "")
    transaction_status = CharField(verbose_name = "交易状态", max_length = 64, choices = TransactionStatus.CHOICES, default = TransactionStatus.SUCCESS)


    update_time = DateTimeField(verbose_name = "更新时间", auto_now = True)
    create_time = DateTimeField(verbose_name = "创建时间", default = timezone.now)

    @classmethod
    def search(cls, **attrs):
        merchant_transaction_qs = cls.query().filter(**attrs)
        return merchant_transaction_qs
