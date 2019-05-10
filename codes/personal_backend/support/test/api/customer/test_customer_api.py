# coding=UTF-8

import json

from support.common.testcase.api_test_case import APITestCase

'''
class Get(APITestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_customer_get(self):
        """test customer to get"""

        flag = "user"
        api = "customer.get"
        customer_id = 1

        result = self.access_api(flag = flag, api = api, customer_id = customer_id)
        self.assertTrue('customer_info' in result)
        print(result["customer_info"])

class Search(APITestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_customer_search(self):
        """test customer to search"""

        flag = "user"
        api = "customer.search"
        current_page = 1
        search_info = json.dumps({

        })

        result = self.access_api(flag = flag, api = api, current_page = current_page, search_info = search_info)
        self.assertTrue('data_list' in result)
        print(result["data_list"])
'''
class Update(APITestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_customer_update(self):
        """test customer to update"""

        flag = "user"
        api = "customer.update"
        customer_id = 1
        customer_info = json.dumps({
            "name":"贾欣远1"
        })

        result = self.access_api(flag = flag, api = api, customer_id = customer_id, customer_info = customer_info)
