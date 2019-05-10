# coding=UTF-8

import json

from support.common.testcase.api_test_case import APITestCase

'''
class Add(APITestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_shop_add(self):
        """test shop to add"""

        flag = "user"
        api = "shop.add"
        import time
        shop_info = json.dumps({
            "name" : "苏宁-开店宝数码专营店" + str(time.time()),
            "single_repair_money": 600,
            "single_point_money": 150,
            "is_distribution": 3,
            "channel_id": 1,
            "remark": ""
        })

        result = self.access_api(flag = flag, api = api, shop_info = shop_info)

class Get(APITestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_shop_get(self):
        """test shop to get"""

        flag = "user"
        api = "shop.get"
        shop_id = 1

        result = self.access_api(flag = flag, api = api, shop_id = shop_id)
        self.assertTrue('shop_info' in result)

class Search(APITestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_shop_search(self):
        """test shop to search"""

        flag = "user"
        api = "shop.search"
        current_page = 1
        search_info = json.dumps({

        })

        result = self.access_api(flag = flag, api = api, current_page = current_page, search_info = search_info)
        self.assertTrue('data_list' in result)
'''
class SearchAll(APITestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_shop_searchall(self):
        """test shop to searchall"""

        flag = "user"
        api = "shop.searchall"
        search_info = json.dumps({

        })

        result = self.access_api(flag = flag, api = api, search_info = search_info)
        self.assertTrue('data_list' in result)
        print(result["data_list"])
'''
class Update(APITestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_shop_update(self):
       """test shop to update"""

       flag = "user"
       api = "shop.update"
       shop_id = 1
       shop_info = json.dumps({
            "name" : "京东店铺1号",
            "single_repair_money": 4304,
            "single_point_money": 8525,
            "is_distribution": 1,
            "channel_id": 1,
            "remark": "京东店铺1号备注22"
        })
       result = self.access_api(flag = flag, api = api, shop_id = shop_id, shop_info = shop_info)

class Remove(APITestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_shop_remove(self):
        """test shop to remove"""

        flag = "user"
        api = "shop.remove"
        shop_id = 1

        result = self.access_api(flag = flag, api = api, shop_id = shop_id)

class Match(APITestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_shop_match(self):
        """test shop to match"""

        flag = "user"
        api = "shop.match"
        keyword = "京东"
        size = 5

        result = self.access_api(flag = flag, api = api, keyword = keyword, size = size)
        self.assertTrue('match_list' in result)
        print(result["match_list"])
'''
