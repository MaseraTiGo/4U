# coding=UTF-8

import json

from support.common.testcase.api_test_case import APITestCase


class Rule(APITestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_rule_list(self):
        """test rule list"""

        api = "permise.staff.rule.list"
        result = self.access_api(api = api)
        self.assertTrue('rule_list' in result)
        print(result)
