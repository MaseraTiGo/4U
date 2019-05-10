# coding=UTF-8

import json

from support.common.testcase.api_test_case import APITestCase

'''
class Add(APITestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_event_track_add(self):
        """test event_track to add"""

        flag = "user"
        api = "event.track.add"
        track_event_info = json.dumps({
            "customer_id" : 1,
            "remark": "测试客户不接电话"
        })

        result = self.access_api(flag = flag, api = api, track_event_info = track_event_info)

class Search(APITestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_event_track_search(self):
        """test event_track to search"""

        flag = "user"
        api = "event.track.search"
        current_page = 1
        search_info = json.dumps({

        })

        result = self.access_api(flag = flag, api = api, current_page = current_page, search_info = search_info)
        self.assertTrue('data_list' in result)
        print(result["data_list"])
'''
class Search(APITestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_event_track_searchbytrack(self):
        """test event_track to searchbytrack"""

        flag = "user"
        api = "event.track.searchbytrack"
        sale_chance_id = 1

        result = self.access_api(flag = flag, api = api, sale_chance_id = sale_chance_id)
        self.assertTrue('data_list' in result)
        print(result["data_list"])
