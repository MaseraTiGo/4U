# coding=UTF-8

import unittest

from tuoen.abs.middleware.extend.saobei.saobei import saobei_extend


class SaobeiMiddleware(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    '''
    def test_get_qrpay_url(self):
        print("===get_qrpay_url")
        dic_param = {"terminal_trace":"FSY202006170002", "terminal_time":"20200617114330", \
                     "total_fee":"1", "body":"邮费", "notify_url":""}
        result = saobei_extend.get_qrpay_url(dic_param)
        print("======result", result)
    '''
    '''
    def test_query(self):
        print("===query")
        dic_param = {"pay_trace":"FSY202006170002", "pay_time":"20200617114330"}
        result = saobei_extend.query(dic_param)
        print("======result", result)
    '''
    '''
    def test_refund(self):
        print("===refund")
        dic_param = {"terminal_trace":"FSY202006170003", "terminal_time":"20200617143330", \
                     "refund_fee":"1", "out_trade_no":"117186261821320061714232504307"}
        result = saobei_extend.refund(dic_param)
        print("======result", result)
    '''
    '''
    def test_queryrefund(self):
        print("===queryrefund")
        dic_param = {"pay_trace":"FSY202006170003", "pay_time":"20200617143330"}
        result = saobei_extend.queryrefund(dic_param)
        print("======result", result)
    '''
