# coding=UTF-8

import json

from support.common.testcase.api_test_case import APITestCase


class Get(APITestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_order_get(self):
        """test order to get"""

        flag = "user"
        api = "order.get"
        order_id = 3

        result = self.access_api(flag = flag, api = api, order_id = order_id)
        self.assertTrue('order_info' in result)
        print(result["order_info"])
'''
class Search(APITestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_order_search(self):
        """test order to search"""

        flag = "user"
        api = "order.search"
        current_page = 1
        search_info = json.dumps({

        })

        result = self.access_api(flag = flag, api = api, current_page = current_page, search_info = search_info)
        self.assertTrue('data_list' in result)
        print(result["data_list"])

class Transfer(APITestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_order_transfer(self):
        """test order to transfer"""

        flag = "user"
        api = "order.transfer"
        order_id = 5
        staff_id = 34
        print("====>>")
        result = self.access_api(flag = flag, api = api, order_id = order_id, staff_id = staff_id)

'''
