# coding=UTF-8

import json

from support.common.testcase.api_test_case import APITestCase


class Search(APITestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_product_search(self):
        """test service_item to search"""

        flag = "user"
        api = "product.product.search"
        current_page = 1
        search_info = json.dumps({
        })

        result = self.access_api(flag = flag, api = api, current_page = current_page, search_info = search_info)
        self.assertTrue('data_list' in result)

class Add(APITestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_product_search(self):
        """test product to add"""

        flag = "user"
        api = "product.product.add"
        current_page = 1
        search_info = json.dumps({
            'name': "可爱的小蓝牙呀"
        })
        print('start------------------------>add')
        result = self.access_api(flag = flag, api = api, current_page = current_page, product_info = search_info)

class Update(APITestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_product_search(self):
        """test product to add"""

        flag = "user"
        api = "product.product.update"
        current_page = 1
        search_info = json.dumps({
            'id': 6,
            'name': '一点都不可爱的蓝牙',
            'alias': "捣乱哟"
        })
        print('start------------------------>update')
        result = self.access_api(flag = flag, api = api, current_page = current_page, product_info = search_info)

class Remove(APITestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_product_remove(self):
        """test product to add"""

        flag = "user"
        api = "product.product.remove"
        current_page = 1
        search_info = json.dumps({
            'id': 12,
        })
        print('start------------------------>remove')
        result = self.access_api(flag = flag, api = api, current_page = current_page, product_info = search_info)

