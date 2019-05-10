# coding=UTF-8

import json

from support.common.testcase.api_test_case import APITestCase


class Search(APITestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_customer_register_search(self):
        """test customer register to search"""

        flag = "user"
        api = "customer.register.search"
        current_page = 1
        search_info = json.dumps({
        'code': 'A004517739'
        })

        result = self.access_api(flag = flag, api = api, current_page = current_page, search_info = search_info)
        self.assertTrue('data_list' in result)
        print(result["data_list"])
'''

class Add(APITestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_sale_chance_add(self):
        """test customer sale_chance to add"""

        flag = "user"
        api = "customer.sale.chance.add"
        sale_chance_info = json.dumps({
            "customer_ids":[1],
            "staff_id":1,
            "goods_id":1,
            "end_time":"2018-05-19 23:59:59"
        })

        result = self.access_api(flag = flag, api = api, sale_chance_info = sale_chance_info)
'''
