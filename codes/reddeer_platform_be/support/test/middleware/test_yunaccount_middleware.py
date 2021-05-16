# coding=UTF-8

import unittest

from tuoen.abs.middleware.extend.yunaccount.yunaccount import yunaccount_extend


class YunaccountMiddleware(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    '''
    def test_verify_identity(self):
        print("===verify_identity")
        result = yunaccount_extend.verify_identity("张三", "1")
        print("======result", result)
    '''
    '''
    def test_verify_bank_card(self):
        print("===verify_bank_card")
        result = yunaccount_extend.verify_bank_card("冯时宇", "420684199010010077", "6214830279698293")
        print("======result", result)
    '''
    '''
    def test_transfers_for_alipay(self):
        print("===transfers_for_alipay")
        dic_param = {"order_id":"FSY202006170001", "real_name":"冯时宇", \
                     "id_card":"420684199010010077", "card_no":"369874203@qq.com", \
                     "pay":"0.01"}
        result = yunaccount_extend.transfers_for_alipay(dic_param)
        print("======result", result)
    '''
    '''
    def test_transfers(self):
        print("===transfers")
        dic_param = {"order_id":"FSY202006170004", "real_name":"冯时宇", \
                     "card_no":"6214830279698293", "phone_no":"13871491385", \
                     "id_card":"420684199010010077", \
                     "pay":"0.01"}
        result = yunaccount_extend.transfers(dic_param)
        print("======result", result)
    '''
