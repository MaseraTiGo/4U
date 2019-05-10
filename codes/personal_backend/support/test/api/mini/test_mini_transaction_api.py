# coding=UTF-8

import json

from support.common.testcase.api_test_case import APITestCase


class Search(APITestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_mini_transaction_search(self):
        """test mini order to search"""

        flag = "mini"
        api = "mini.transaction.search"
        sn_list = json.dumps(['760300010483746'])
        search_info = json.dumps({
            "transaction_time_start":"2018-07-01 00:00:00",
            "transaction_time_end":"2018-07-10 23:59:59",
        })


        result = self.access_api(flag = flag, api = api, sn_list = sn_list, \
                                search_info = search_info)

        print(result["data_list"])
