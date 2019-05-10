# coding=UTF-8

import json

from support.common.testcase.api_test_case import APITestCase

'''
class Add(APITestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_staff_departmentchange_add(self):
        """test staff departmentchange to add"""

        flag = "user"
        api = "permise.staff.departmentchange.add"
        department_change_info = json.dumps({
            "staff_id" : 579,
            "department_front_id" : 34,
            "department_now_id": 35,
            "start_time": "2018-07-11 00:00:00",
            "end_time": "2018-07-11 23:59:59",
            "remark": "",
        })

        result = self.access_api(flag = flag, api = api, department_change_info = department_change_info)
'''
class Search(APITestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_staff_departmentchange_search(self):
        """test staff departmentchange to search"""

        flag = "user"
        api = "permise.staff.departmentchange.search"
        current_page = 1
        search_info = json.dumps({
            "keyword":"肖术芹"
        })
        result = self.access_api(flag = flag, api = api, \
                                 current_page = current_page, \
                                 search_info = search_info)
        self.assertTrue('data_list' in result)
        print(result["data_list"])

'''
class Get(APITestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_staff_departmentchange_get(self):
        """test staff departmentchange to get"""

        flag = "user"
        api = "permise.staff.departmentchange.get"
        department_change_id = 1

        result = self.access_api(flag = flag, api = api, \
                                 department_change_id = department_change_id)
        self.assertTrue('department_change_info' in result)
        print(result["department_change_info"])

class Update(APITestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_staff_departmentchange_update(self):
        """test staff departmentchange update"""

        flag = "user"
        api = "permise.staff.departmentchange.update"
        department_change_id = 1
        department_change_info = json.dumps({
            "staff_id" : 18,
            "department_front_id" : 2,
            "department_now_id": 3,
            "start_time": "2018-07-01 00:00:00",
            "end_time": "2018-07-01 23:59:59",
            "remark": "1111111",
       })

        result = self.access_api(flag = flag, api = api, \
                                 department_change_id = department_change_id, \
                                 department_change_info = department_change_info)

class Remove(APITestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_staff_departmentchange_remove(self):
        """test staff departmentchange remove"""

        flag = "user"
        api = "permise.staff.departmentchange.remove"
        department_change_id = 1

        result = self.access_api(flag = flag, api = api, \
                                 department_change_id = department_change_id)

class Executed(APITestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_staff_departmentchange_executed(self):
        """test staff departmentchange executed"""

        flag = "user"
        api = "permise.staff.departmentchange.executed"
        department_change_id = 1

        result = self.access_api(flag = flag, api = api, \
                                 department_change_id = department_change_id)
'''
