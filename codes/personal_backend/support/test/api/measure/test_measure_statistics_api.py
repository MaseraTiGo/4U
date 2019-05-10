# coding=UTF-8

import json

from support.common.testcase.api_test_case import APITestCase


class MeasureStatistics(APITestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_measure_search(self):
        """test measure to statistics search """
        current_page = 1
        search_info = json.dumps({
            'begin_time': '2018-07-01 00:00:00',
            'end_time': '2018-07-10 00:00:00',

        })
        flag = "user"
        api = "measure.statistics.search"

        result = self.access_api(flag=flag, api=api, search_info=search_info, current_page=current_page)
        # self.assertTrue('data_list' in result)
        # print(result["data_list"])
        # print(result["sum_measure_data"])
        print('----------------->', result)

    def test_measure_statistics(self):
        """test measure to statistics"""

        search_info = json.dumps({
            'begin_time': '2018-07-01 00:00:00',
            'end_time': '2018-07-10 00:00:00',

        })
        flag = "user"
        api = "measure.statistics.statistics"

        result = self.access_api(flag=flag, api=api, search_info=search_info)
        # self.assertTrue('data_list' in result)
        # print(result["data_list"])
        # print(result["sum_measure_data"])
        print('----------------->', result)
