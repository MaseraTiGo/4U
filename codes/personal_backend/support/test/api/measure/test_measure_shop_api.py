# coding=UTF-8

import json

from support.common.testcase.api_test_case import APITestCase

'''
class Add(APITestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_measure_shop_add(self):
        """test measure shop to add"""

        flag = "user"
        api = "measure.shop.add"
        report_info = json.dumps({
            "shop_id" : 2,
            "total_sales": 100,
            "add_order_number": 100,
            "through_number": 100,
            "through_money" : 10000,
            "record_date": "2018-05-12 18:22:23",
            "remark": ""
        })

        result = self.access_api(flag = flag, api = api, report_info = report_info)

class Get(APITestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_measure_shop_get(self):
        """test measure shop to get"""

        flag = "user"
        api = "measure.shop.get"
        report_id = 8

        result = self.access_api(flag = flag, api = api, report_id = report_id)
        self.assertTrue('report_info' in result)

'''
class Search(APITestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_measure_shop_search(self):
        """test measure shop to search"""

        flag = "user"
        api = "measure.shop.search"
        current_page = 2
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

    def test_measure_shop_update(self):
       """test measure shop to update"""

       flag = "user"
       api = "measure.shop.update"
       report_id = 8
       report_info = json.dumps({
            "shop_id" : 2,
            "total_sales": 100,
            "add_order_number": 100,
            "through_number": 100,
            "through_money" : 10000,
            "record_date": "2018-05-12 18:22:23",
            "remark": "测试"
        })
       result = self.access_api(flag = flag, api = api, report_id = report_id, report_info = report_info)

class Remove(APITestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_measure_shop_remove(self):
        """test measure shop to remove"""

        flag = "user"
        api = "measure.shop.remove"
        report_id = 8

        result = self.access_api(flag = flag, api = api, report_id = report_id)


class Statistics(APITestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_measure_shop_statistics(self):
        """test measure shop to statistics"""

        flag = "user"
        api = "measure.shop.statistics"
        current_page = 1
        search_info = json.dumps({

        })

        result = self.access_api(flag = flag, api = api, current_page = current_page, search_info = search_info)
        self.assertTrue('data_list' in result)
        print(result["data_list"])
'''
