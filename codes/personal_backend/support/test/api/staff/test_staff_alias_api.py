# coding=UTF-8

import json

from support.common.testcase.api_test_case import APITestCase

'''
class Add(APITestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_staffalias_add(self):
        """test shop channel to add"""

        flag = "user"
        api = "staffalias.add"
        alias_info = json.dumps({
            "staff_id" : 1,
            "alias": "李小四",
            "remark": "",
        })

        result = self.access_api(flag = flag, api = api, alias_info = alias_info)

class Search(APITestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_staffalias_search(self):
        """test staffalias to search"""

        flag = "user"
        api = "staffalias.search"
        current_page = 1
        search_info = json.dumps({

        })

        result = self.access_api(flag = flag, api = api, current_page = current_page, search_info = search_info)
        self.assertTrue('data_list' in result)
        print(result["data_list"])

class Update(APITestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_staffalias_update(self):
       """test staffalias to update"""

       flag = "user"
       api = "staffalias.update"
       staff_alias_id = 1
       alias_info = json.dumps({
           "alias": "张小三",
           "remark": "测试备注"
       })
       result = self.access_api(flag = flag, api = api, staff_alias_id = staff_alias_id, \
                                alias_info = alias_info)

class Remove(APITestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_staffalias_remove(self):
        """test staffalias to remove"""

        flag = "user"
        api = "staffalias.remove"
        staff_alias_id = 2

        result = self.access_api(flag = flag, api = api, staff_alias_id = staff_alias_id)
'''
