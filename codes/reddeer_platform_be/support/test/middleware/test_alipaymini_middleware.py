# coding=UTF-8

import unittest

from tuoen.abs.middleware.extend.alipay.alipay_mini import alipay_mini_extend


class AlipayminiMiddleware(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_get_chance_qrcode(self):
        print("===get_chance_qrcode")
        dic_param = {"url_param":"/alipya/index", "data":{"aa":"1"}, \
                     "describe":"商品"}
        result = alipay_mini_extend.get_chance_qrcode(**dic_param)
        print("======result", result)

    '''
    def test_get_chance_qrcode(self):
        print("===get_chance_qrcode")
        dic_param = {"url_param":"/alipya/index", "data":{"aa":"1"}, \
                     "describe":"商品"}
        result = alipay_mini_extend.get_chance_qrcode(**dic_param)
        print("======result", result)
    '''
    '''
    def test_get_user_id(self):
        print("===get_user_id")
        dic_param = {"code":"FSY202006170002"}
        result = alipay_mini_extend.get_user_id(dic_param)
        print("======result", result)
    '''
    '''
    def test_alipay_freeze_query(self):
        print("===alipay_freeze_query")
        dic_param = {"auth_no":"FSY202006170003", "operation_id":"20200617143330"}
        result = alipay_mini_extend.alipay_freeze_query(**dic_param)
        print("======result", result)
    '''
    '''
    def test_alipay_unfreeze(self):
        print("===alipay_unfreeze")
        dic_param = {"auth_no":"FSY202006170003", "amount":100, \
                     "deposit_type":"credit"}
        result = alipay_mini_extend.alipay_unfreeze(**dic_param)
        print("======result", result)
    '''
    '''
    def test_alipay_freeze_trade(self):
        print("===alipay_freeze_trade")
        dic_param = {"auth_no":"FSY202006170003", "buyer_id":"1231321", \
                     "seller_id":"12321321321", "total_amount":100}
        result = alipay_mini_extend.alipay_freeze_trade(**dic_param)
        print("======result", result)
    '''
    '''
    def test_alipay_freeze(self):
        print("===alipay_freeze")
        dic_param = {"order_no":"FSY202006170003", "amount":100}
        result = alipay_mini_extend.alipay_freeze(**dic_param)
        print("======result", result)
    '''
