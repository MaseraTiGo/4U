# coding=UTF-8

import json

from support.common.testcase.api_test_case import APITestCase
from support.simulate.staff import StaffMaker


class Search(APITestCase):

    def setUp(self):
        staff_generators = StaffMaker().run()
        staff_generator = staff_generators[0]
        self._staff = staff_generator.get_result()[0]

    def tearDown(self):
        pass

    def test_search(self):
        """ test journal to Search """

        flag = "user"
        api = "journal.search"
        current_page = 1
        search_info = json.dumps({
            "active_name" : self._staff.name,
            "active_type" : "staff",
            "passive_name" : self._staff.name,
            "passive_type" : "user",
            "journal_type" : "other",
            "start_time" : "2018-04-11 10:31:00",
            "end_time" : "2018-05-13 10:31:00",
        })

        result = self.access_api(flag = flag, api = api, current_page = current_page, search_info = search_info)
        self.assertTrue('data_list' in result)
