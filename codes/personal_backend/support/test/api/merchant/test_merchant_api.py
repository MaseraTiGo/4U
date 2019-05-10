# coding=UTF-8

import json

from support.common.testcase.api_test_case import APITestCase

'''
class Add(APITestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_merchant_add(self):
        """test merchant to add"""

        flag = "user"
        api = "merchant.add"
        merchantId = "212139508409952"
        merchantName = "fsy"
        organId = "88888888"
        organName = "test"
        organLevel = "3"
        realName = "fsy"
        idCard = "350111198802011133"
        phone = "15888888888"
        regDate = "20180904101600"
        serialNo = "7016738939"
        terminalId = "23221113"
        bindingDate = "20180304221132"
        pid = "11"

        result = self.access_api(flag = flag, api = api, \
                                 merchantId = merchantId, merchantName = merchantName, \
                                 organId = organId, organName = organName, \
                                 organLevel = organLevel, realName = realName, \
                                 idCard = idCard, phone = phone, \
                                 regDate = regDate, serialNo = serialNo, \
                                 terminalId = terminalId, bindingDate = bindingDate, \
                                 pid = pid)
'''

class Add(APITestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_merchant_transaction_add(self):
        """test merchant_transaction to add"""

        flag = "user"
        api = "merchant.transaction.add"
        merchantId = "212139508409952"
        organId = "88888888"
        serialNo = "7016738939"
        terminalId = "23221113"
        transId = "31231232133323423423423"
        transType = "2"
        txDate = "20180904101600"
        txAmt = "0000000500000"
        actAmt = "0000000499500"
        orderNo = "124578844512"
        pid = "11"

        result = self.access_api(flag = flag, api = api, \
                                 merchantId = merchantId, organId = organId, \
                                 serialNo = serialNo, terminalId = terminalId, \
                                 transId = transId, transType = transType, \
                                 txDate = txDate, txAmt = txAmt, \
                                 actAmt = actAmt, orderNo = orderNo, \
                                 pid = pid)

