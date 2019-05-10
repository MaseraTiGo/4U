# coding=UTF-8

# coding=UTF-8

'''
Created on 2016年7月23日

@author: Administrator
'''
import datetime

from tuoen.sys.core.field.base import CharField, DictField, IntField, ListField, DatetimeField, DateField
from tuoen.sys.core.api.utils import with_metaclass
from tuoen.sys.core.api.request import RequestField, RequestFieldSet
from tuoen.sys.core.api.response import ResponseField, ResponseFieldSet
from tuoen.sys.core.exception.business_error import BusinessError

from tuoen.agile.apis.base import StaffAuthorizedApi
from tuoen.abs.service.merchant.manager import MerchantServer, MerchantTransactionServer
from tuoen.abs.service.equipment.manager import EquipmentSnServer


class Add(StaffAuthorizedApi):
    """添加流水"""
    request = with_metaclass(RequestFieldSet)
    request.merchantId = RequestField(CharField, desc = "商户编号")
    request.organId = RequestField(CharField, desc = "机构编号")
    request.serialNo = RequestField(CharField, desc = "硬件系列号")
    request.terminalId = RequestField(CharField, desc = "终端编号")
    request.transId = RequestField(CharField, desc = "交易编号")
    request.transType = RequestField(CharField, desc = "交易类型")
    request.txDate = RequestField(CharField, desc = "交易时间")
    request.txAmt = RequestField(CharField, desc = "交易金额")
    request.actAmt = RequestField(CharField, desc = "实际到账金额")
    request.orderNo = RequestField(CharField, desc = "交易参考号或订单号")
    request.pid = RequestField(CharField, desc = "产品编号")


    response = with_metaclass(ResponseFieldSet)
    response.respCode = CharField(desc = "应答码")
    response.respMsg = CharField(desc = "应答描述")


    @classmethod
    def get_desc(cls):
        return "商户流水推送获取接口"

    @classmethod
    def get_author(cls):
        return "fsy"

    def execute(self, request):
        merchant = MerchantServer.get_merchant_bymid(request.merchantId)
        if merchant is not None:
            tx_date = datetime.datetime.strptime(request.txDate, '%Y%m%d%H%M%S')
            if not MerchantTransactionServer.is_exit(**{"merchant_sn":request.merchantId, "tx_date":tx_date}):
                merchant_transaction_info = {"merchant":merchant, \
                                             "merchant_sn":request.merchantId, "organ_id":request.organId, \
                                             "serial_no":request.serialNo, "terminal_id":request.terminalId, \
                                             "trans_id":request.transId, "trans_type":int(request.transType), \
                                             "tx_date":datetime.datetime.strptime(request.txDate, '%Y%m%d%H%M%S'), \
                                             "tx_amt":int(request.txAmt), "act_amt":int(request.actAmt), \
                                             "tx_ref_id":request.orderNo  if int(request.transType) != 3 else "", \
                                             "order_no":request.orderNo if int(request.transType) == 3 else "", \
                                             "pid":request.pid}
                MerchantTransactionServer.generate(**merchant_transaction_info)

                if MerchantTransactionServer.check_is_activation(merchant):
                    merchant.update(is_activation = 1)

    def fill(self, response):
        response.respCode = "0000"
        response.respMsg = "操作成功"
        return response
