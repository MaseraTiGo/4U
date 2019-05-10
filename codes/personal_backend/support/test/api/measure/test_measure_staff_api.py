# coding=UTF-8

import json

from support.common.testcase.api_test_case import APITestCase

'''
class Add(APITestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_measure_staff_add(self):
        """test measure staff to add"""

        flag = "user"
        api = "measure.staff.add"
        measure_staff_info = json.dumps({
            "staff_id" : 1,
            "new_number": 100,
            "exhale_number": 80,
            "call_number": 40,
            "wechat_number" : 100,
            "report_date": "2018-05-12 18:22:23",
            "remark": ""
        })

        result = self.access_api(flag = flag, api = api, measure_staff_info = measure_staff_info)

class Get(APITestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_measure_staff_get(self):
        """test measure staff to get"""

        flag = "user"
        api = "measure.staff.get"
        measure_staff_id = 1

        result = self.access_api(flag = flag, api = api, measure_staff_id = measure_staff_id)
        self.assertTrue('measure_staff_info' in result)


class Search(APITestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_measure_staff_search(self):
        """test measure staff to search"""

        flag = "user"
        api = "measure.staff.search"
        current_page = 1
        search_info = json.dumps({

        })

        result = self.access_api(flag = flag, api = api, current_page = current_page, search_info = search_info)
        self.assertTrue('data_list' in result)
        print(result)

class Update(APITestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_measure_staff_update(self):
       """test measure staff to update"""

       flag = "user"
       api = "measure.staff.update"
       measure_staff_id = 1
       measure_staff_info = json.dumps({
            "staff_id" : 1,
            "new_number": 100,
            "exhale_number": 80,
            "call_number": 40,
            "wechat_number" : 100,
            "report_date": "2018-05-12 18:22:23",
            "remark": "测试"
        })
       result = self.access_api(flag = flag, api = api, measure_staff_id = measure_staff_id, measure_staff_info = measure_staff_info)

class Remove(APITestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_measure_staff_remove(self):
        """test measure staff to remove"""

        flag = "user"
        api = "measure.staff.remove"
        measure_staff_id = 1

        result = self.access_api(flag = flag, api = api, measure_staff_id = measure_staff_id)
'''

class Statistics(APITestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_measure_staff_statistics(self):
        """test measure staff to statistics"""

        flag = "user"
        api = "measure.staff.statistics"
        current_page = 1
        search_info = json.dumps({

        })

        result = self.access_api(flag = flag, api = api, current_page = current_page, search_info = search_info)
