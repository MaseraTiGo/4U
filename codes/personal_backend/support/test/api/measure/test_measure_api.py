# coding=UTF-8

import json

from support.common.testcase.api_test_case import APITestCase


class Statistics(APITestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_measure_statistics(self):
        """test measure to statistics"""

        flag = "user"
        api = "measure.statistics"

        result = self.access_api(flag = flag, api = api)
        self.assertTrue('data_list' in result)
        print(result["data_list"])
