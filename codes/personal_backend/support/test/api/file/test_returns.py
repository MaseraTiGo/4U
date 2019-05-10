# coding=UTF-8

import os
import json

from support.common.testcase.api_test_case import APITestCase


class ReturnsUpload(APITestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass
    def test_returns_reset(self):
        api = "data.returns.resetsatus"#"data.equipmentin.resetsatus"#"data.buyinfo.resetsatus"#
        buyinfo_id = '[6, 7]'
        search_info = json.dumps({
            'ids': '[1]'
        })
        result = self.access_file_api(api, store_type="test", flag="user", search_info=search_info)
        self.assertTrue(result is None)
        print("-------------------->test result<<<", result)
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


    
