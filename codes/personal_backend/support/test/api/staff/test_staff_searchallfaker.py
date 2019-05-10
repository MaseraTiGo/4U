# coding=UTF-8

import json
import datetime

from support.common.testcase.api_test_case import APITestCase
from support.common.tools.utils import *
from support.common.constants import GenderTypes
from model.models import Staff

class Search(APITestCase):

    def setup(self):
        pass

    def teardown(self):
        pass

    def test_staff_measure(self):
        api = "user.staff.searchallfaker"
        search_info = json.dumps({})
        current_page = 1
        cur_user = Staff.query().filter(phone='13682286629')[0]
        result = self.access_api(api = api, cur_user=cur_user, search_info = search_info,\
                                 current_page = current_page)
        self.assertTrue('data_list' in result)
        print("sub_info_list:::", len(result['data_list']))
