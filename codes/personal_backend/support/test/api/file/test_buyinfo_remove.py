# coding=UTF-8

import os
import json

from support.common.testcase.api_test_case import APITestCase


class BuyInfoResetStatus(APITestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass
    def test_buyinfo_resetstatus(self):
        api = "data.buyinfo.resetsatus"
        ids = json.dumps([1, 8, 10, 11])
        search_info = json.dumps({
            "create_time_start": "2018-06-01 00:00:00",
            "create_time_end": "2018-06-27 18:03:17"}
        )
        result = self.access_file_api(api, store_type="test", flag="user", ids=ids, search_info=search_info)
        self.assertTrue(result is None)
'''
    def test_returns_search(self):
        api = "data.returns.search"
        current_page = 1
        search_info = json.dumps({

        })
        result = self.access_file_api(api, store_type="test", current_page=current_page, flag="user", search_info=search_info)
        print("-------------------->test result", result)
    
    def test_returns_upload_file(self):
        print("--------------->start")
        cur_path = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(cur_path, 'returns_upload.xlsx')
        files = {'returns_upload.xlsx': open(file_path, 'rb')}
        api = "data.returns.upload"
        result = self.access_file_api(api, files = files, store_type = "test", flag = "user")
        print("-------------------->test result", result)
'''


    
