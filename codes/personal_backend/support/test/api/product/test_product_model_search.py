# coding=UTF-8

import json

from support.common.testcase.api_test_case import APITestCase
from model.models import Product


class Search(APITestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_product_model_search(self):
        """test product model to search"""

        flag = "user"
        api = "product.productmodel.search"
        current_page = 1
        search_info = json.dumps({
        })

        result = self.access_api(flag = flag, api = api, current_page = current_page, search_info = search_info)
        self.assertTrue('data_list' in result)
        print('------------------------------>', result["data_list"])

class Add(APITestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_product_search(self):
        """test product model to add"""

        flag = "user"
        api = "product.productmodel.add"
        current_page = 1
        search_info = json.dumps({
            'name': "DS-666",
            'product': 2
        })
        print('start------------------------>add')
        result = self.access_api(flag = flag, api = api, current_page = current_page, product_model_info = search_info)

class Update(APITestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_product_search(self):
        """test product model to update"""

        flag = "user"
        api = "product.productmodel.update"
        current_page = 1
        product_id = 6
        #product = Product.get_byid(product_id)
        search_info = json.dumps({
            'id': 23,
            'name': "T-800",
            'remark': "terminatorGOGOGO"
        })
        print('search_info==================>>>', search_info)
        #search_info.update({'product': product})
        print('start------------------------>update')
        result = self.access_api(flag = flag, api = api, current_page = current_page, product_info = search_info)

class Remove(APITestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_product_remove(self):
        """test product model to remove"""

        flag = "user"
        api = "product.productmodel.remove"
        current_page = 1
        search_info = json.dumps({
            'id': 12,
        })
        print('start------------------------>remove')
        result = self.access_api(flag = flag, api = api, current_page = current_page, product_info = search_info)
