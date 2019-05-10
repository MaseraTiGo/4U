# coding=UTF-8

import json

from support.common.testcase.api_test_case import APITestCase

'''
class Add(APITestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_account_staff_add(self):
        """test account staff to add"""

        flag = "user"
        api = "account.staff.add"
        user_info = json.dumps({
            'username': "fengshiyu002",
            'name': "冯时宇002",
            'birthday': "2018-04-16",
            'phone': "15232626262",
            'email': "2058556456@qq.com",
            'gender': "man",
            'number': "008",
            'identity': "123456789",
            'role_ids' :[1,17],
            'department_ids' :[1,7],
        })

        result = self.access_api(flag = flag, api = api, user_info = user_info)
        
class UpdatePassword(APITestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass
        
    def test_account_staff_update_password(self):
        """test account staff to update password"""

        flag = "user"
        api = "account.staff.update.password"
        uid = 2
        newpassword = "e10adc3949ba59abbe56e057f20f883e"
        oldpassword = "123456"

        result = self.access_api(flag = flag, api = api, oldpassword = oldpassword, \
            newpassword = newpassword)
'''
class Generate(APITestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_account_staff_generate(self):
        """test account staff to generate"""

        flag = "user"
        api = "account.staff.generate"
        staff_id = 11
        username = "fsy"

        result = self.access_api(flag = flag, api = api, staff_id = staff_id)
