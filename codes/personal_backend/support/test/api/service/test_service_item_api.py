# coding=UTF-8

import json

from support.common.testcase.api_test_case import APITestCase

class EditSn(APITestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_service_item_search(self):
        """test service_item to edit sn"""

        flag = "user"
        api = "service.item.editsn"
        #current_page = 1
        search_info = json.dumps({
        })
        sn_pre = '730300010036664'#'730300010034444'
        sn_after = '730300010036665'#'730300010033333'
        result = self.access_api(flag = flag, api = api, sn_pre=sn_pre, sn_after=sn_after)
        #self.assertTrue('data_list' in result)
        #print(result["data_list"])

# class Search(APITestCase):
#
#     def setUp(self):
#         pass
#
#     def tearDown(self):
#         pass
#
#     def test_service_item_search(self):
#         """test service_item to search"""
#
#         flag = "user"
#         api = "service.item.search"
#         current_page = 1
#         search_info = json.dumps({
#
#         })
#
#         result = self.access_api(flag = flag, api = api, current_page = current_page, search_info = search_info)
#         self.assertTrue('data_list' in result)
#         print(result["data_list"])

'''
class Get(APITestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_service_item_get(self):
        """test service_item to get"""

        flag = "user"
        api = "service.item.get"
        service_item_id = 1

        result = self.access_api(flag = flag, api = api, service_item_id = service_item_id)
        self.assertTrue('service_item_info' in result)
        print(result["service_item_info"])


class Statistics(APITestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_service_item_statistics(self):
        """test service_item to statistics"""

        flag = "user"
        api = "service.item.statistics"
        search_info = json.dumps({

        })

        result = self.access_api(flag = flag, api = api, search_info = search_info)
        self.assertTrue('sum_data' in result)
        print(result["sum_data"])
'''
