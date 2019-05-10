# coding=UTF-8

import json

from support.common.testcase.api_test_case import APITestCase

'''
class Search(APITestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_shop_goods_search(self):
        """test shop goods to search"""

        flag = "user"
        api = "shop.goods.search"
        current_page = 1
        search_info = json.dumps({

        })

        result = self.access_api(flag = flag, api = api, current_page = current_page, search_info = search_info)
        self.assertTrue('data_list' in result)
        print(result["data_list"])

class Match(APITestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_shop_goods_match(self):
        """test shop goods to match"""

        flag = "user"
        api = "shop.goods.match"
        keyword = "大蓝牙"
        size = 5

        result = self.access_api(flag = flag, api = api, keyword = keyword, size = size)
        self.assertTrue('match_list' in result)
        print(result["match_list"])

'''

class SearchAll(APITestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_shop_goods_searchall(self):
        """test shop goods to searchall"""

        flag = "user"
        api = "shop.goods.searchall"

        result = self.access_api(flag = flag, api = api)
        self.assertTrue('data_list' in result)
        print(result["data_list"])
