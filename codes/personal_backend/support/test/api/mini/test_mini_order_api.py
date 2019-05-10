# coding=UTF-8

import json

from support.common.testcase.api_test_case import APITestCase


class Search(APITestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_mini_order_search(self):
        """test mini order to search"""

        flag = "mini"
        api = "mini.order.search"
        order_sn_list = json.dumps(['SO_15309569711391310041', 'SO_15309573890039100463'])

        result = self.access_api(flag = flag, api = api, order_sn_list = order_sn_list)

        print(result["data_list"])
