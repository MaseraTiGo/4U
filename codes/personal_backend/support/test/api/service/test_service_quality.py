# coding=UTF-8

import json

from support.common.testcase.api_test_case import APITestCase


class Search(APITestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_quality_search(self):
        """test service_item to search"""

        flag = "user"
        api = "service.quality.search"
        current_page = 1
        search_info = json.dumps({
        #'name': "伍毅",
        #'equipment_code': "720300010031746",
        "order_sn": "E2016111601120899286",
        #"shop_name": "微信公众号",
        })
        print("===============start================")
        result = self.access_api(flag = flag, api = api, current_page = current_page, search_info = search_info)
        self.assertTrue('data_list' in result)
        print("-------------->final result", result['data_list'])

