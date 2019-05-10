# coding=UTF-8

import json
import datetime

from support.common.testcase.api_test_case import APITestCase
from support.common.tools.utils import *
from support.common.constants import GenderTypes

'''
class Add(APITestCase):

    def test_staff_add(self):
        """ test staff to add """

        api = "user.staff.add"
        user_info = {
            "name" : add_suffix("yrk"),
            "birthday" : serializable_date(1990,7,7),
            "phone" : "15527703115",
            "email" : "7718279@qq.com",
            "gender" : GenderTypes.MAN,
            "number" : "88888",
            "identity" : generate_identity(),
            "emergency_contact" : "杨荣凯",
            "emergency_phone" : "15527701111",
            "address" : "88888",
            "entry_time" : serializable_date(2018,3,22),
            # "education" : "大专",
            # "bank_number" : "1121 2212 3332 1122",
            "expire_time" : serializable_date(2019,3,22),
            "contract_b" : "11111111",
            "contract_l" : "21111111",
            "is_working" : "1",
            "role_ids" : [],
            "department_ids" : [],
        }
        # import pprint
        # pprint.pprint(user_info)
        user_info = json.dumps(user_info)

        result = self.access_api(api = api, user_info = user_info)


class Match(APITestCase):

    def setup(self):
        pass

    def teardown(self):
        pass

    def test_staff_match(self):
        match_list = ['y','rk', 'test']

        api = "user.staff.match"
        size = 5
        for keyword in match_list:
            result = self.access_api(api = api, keyword = keyword, size = size)
            self.assertTrue('match_list' in result)
'''

class Search(APITestCase):

    def setup(self):
        pass

    def teardown(self):
        pass

    def test_staff_search(self):
        api = "service.item.search"#"user.staff.search"
        current_page = 1
        search_info = json.dumps({
            'keyword': '1552770'
        })

        result = self.access_api(api = api, search_info = search_info,\
                                 current_page = current_page)
        self.assertTrue('data_list' in result)
'''
class Show(APITestCase):

    def setup(self):
        pass

    def teardown(self):
        pass

    def test_staff_show(self):
        api = "user.staff.show"
        #current_page = 1
        search_info = json.dumps({
            'keyword': '1552770'
        })

        result = self.access_api(api = api, )
        print("==================>retsult", result)
        #self.assertTrue('data_list' in result)
'''