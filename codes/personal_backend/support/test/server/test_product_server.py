# coding=UTF-8

import unittest

from tuoen.abs.service.product import ProductOperateServer
from tuoen.abs.service.product import ProductModelServer
from model.models import Product

class TestProductServer(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_product_search(self):
        """ test product search """
        account, password = "yangrongkai", "123456"
        current_page = 1
        attrs = {}
        result = ProductOperateServer.search(current_page, **attrs)
        print('----------------->', type(result), result)

    def test_product_add(self):
        """test product_model add new type"""
        product = Product.get_byid(1)
        attrs = {'name': '不大不小蓝牙'}
        ProductOperateServer.add(**attrs)

class TestProductModelServer(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_product_model_search(self):
        """ test product mdoel search """
        account, password = "yangrongkai", "123456"
        current_page = 1
        attrs = {}
        result = ProductModelServer.search(current_page, **attrs)
        print('----------------->', type(result), result)

    def test_product_model_add(self):
        """test product_model add new type"""
        product = Product.get_byid(1)
        attrs = {'name': 'DS-001', 'stock': 1000, 'product': product}
        ProductModelServer.add(**attrs)
