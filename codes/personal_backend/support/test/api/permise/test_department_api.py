# coding=UTF-8

import json

from support.common.testcase.api_test_case import APITestCase

'''
class Add(APITestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_staff_department_add(self):
        """test staff department to add"""

        flag = "user"
        api = "permise.staff.department.add"
        department_info = json.dumps({
            "name" : "测试部门",
            "parent_id" : 0,
            "describe": "测试部门"
        })

        result = self.access_api(flag = flag, api = api, department_info = department_info)
'''
class List(APITestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_staff_department_list(self):
        """test staff department to list"""

        flag = "user"
        api = "permise.staff.department.list"

        result = self.access_api(flag = flag, api = api)
        self.assertTrue('data_list' in result)
        print(result["data_list"])
'''
class Get(APITestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_staff_department_get(self):
        """test staff department to get"""

        flag = "user"
        api = "permise.staff.department.get"
        department_id = 7

        result = self.access_api(flag = flag, api = api, department_id = department_id)
        self.assertTrue('department_info' in result)

class Update(APITestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_staff_department_update(self):
        """test staff department update"""

        flag = "user"
        api = "permise.staff.department.update"
        department_id = 7
        department_info = json.dumps({
            "name" : "测试部门4444",
            "parent_id" : 0,
            "describe": "测试部门4444"
       })

        result = self.access_api(flag = flag, api = api, department_id = department_id, department_info = department_info)

class Remove(APITestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_staff_department_remove(self):
        """test staff department remove"""

        flag = "user"
        api = "permise.staff.department.remove"
        department_id = 16

        result = self.access_api(flag = flag, api = api, department_id = department_id)
'''
