# coding=UTF-8

import json

from support.common.testcase.api_test_case import APITestCase

'''
class Add(APITestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_shop_channel_add(self):
        """test shop channel to add"""

        flag = "user"
        api = "shop.channel.add"
        channel_info = json.dumps({
            "name" : "苏宁",
            "single_repair_money": 600,
            "single_point_money": 150,
            "remark": ""
        })

        result = self.access_api(flag = flag, api = api, channel_info = channel_info)

class Get(APITestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_shop_channel_get(self):
        """test shop channel to get"""

        flag = "user"
        api = "shop.channel.get"
        channel_id = 1

        result = self.access_api(flag = flag, api = api, channel_id = channel_id)
        self.assertTrue('channel_info' in result)

class Search(APITestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_shop_channel_search(self):
        """test shop channel to search"""

        flag = "user"
        api = "shop.channel.search"
        current_page = 1
        search_info = json.dumps({
            "name" : "苏宁",
        })

        result = self.access_api(flag = flag, api = api, current_page = current_page, search_info = search_info)
        self.assertTrue('data_list' in result)

class Update(APITestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_shop_channel_update(self):
       """test shop channel to update"""

       flag = "user"
       api = "shop.channel.update"
       channel_id = 2
       channel_info = json.dumps({
           "name" : "京东",
           "single_repair_money": 123,
           "single_point_money": 123,
           "remark": "测试备注"
       })
       result = self.access_api(flag = flag, api = api, channel_id = channel_id, channel_info = channel_info)

class Remove(APITestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_shop_channel_remove(self):
        """test shop channel to remove"""

        flag = "user"
        api = "shop.channel.remove"
        channel_id = 1

        result = self.access_api(flag = flag, api = api, channel_id = channel_id)

class Match(APITestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_shop_channel_match(self):
        """test shop channel to match"""

        flag = "user"
        api = "shop.channel.match"
        keyword = "京"
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

    def test_shop_channel_searchall(self):
        """test shop channel to searchall"""

        flag = "user"
        api = "shop.channel.searchall"
        search_info = json.dumps({

        })

        result = self.access_api(flag = flag, api = api, search_info = search_info)
        self.assertTrue('data_list' in result)
        print(result["data_list"])
