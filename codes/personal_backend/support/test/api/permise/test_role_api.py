# coding=UTF-8

import json

from support.common.testcase.api_test_case import APITestCase


class List(APITestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_staff_role_list(self):
        """test staff role to list"""

        flag = "user"
        api = "permise.staff.role.list"

        result = self.access_api(flag = flag, api = api)
        self.assertTrue('data_list' in result)
        print(result['data_list'])

class Get(APITestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_staff_role_get(self):
        """test staff role to get"""

        flag = "user"
        api = "permise.staff.role.get"
        role_id = 15

        result = self.access_api(flag = flag, api = api, role_id = role_id)
        self.assertTrue('role_info' in result)

class Update(APITestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_staff_role_update(self):
        """test staff role to update"""

        flag = "user"
        api = "permise.staff.role.update"
        role_id = 15
        role_info = json.dumps({
            "name" : "测试管理员22222",
            "parent_id" : 0,
            "rules" : "1,2,3,4",
            "describe": "测试管理员22222",
            "is_show_data": 1
       })

        result = self.access_api(flag = flag, api = api, role_id = role_id, role_info = role_info)

class Remove(APITestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_staff_role_remove(self):
        """test staff role to remove"""

        flag = "user"
        api = "permise.staff.role.remove"
        role_id = 15

        result = self.access_api(flag = flag, api = api, role_id = role_id)
