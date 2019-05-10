# coding=UTF-8

import json

from support.common.testcase.api_test_case import APITestCase


class TestStaffLogin(APITestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_account_staff_login(self):
        """test account staff to add"""

        api = "account.staff.login"
        username = '15527703115'
        password = '15527703115'

        result = self.access_api(api = api, username = username, password = password)
        self.assertTrue('auth_token' in result)
        self.assertTrue('renew_flag' in result)
        self.assertTrue('department_list' in result)
        self.assertTrue('role_list' in result)
        self.assertTrue('rule_list' in result)
