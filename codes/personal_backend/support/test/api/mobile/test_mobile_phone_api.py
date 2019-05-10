# coding=UTF-8

import json
import datetime

from support.common.testcase.api_test_case import APITestCase
from support.common.tools.utils import *
from support.common.constants import GenderTypes

'''
class Add(APITestCase):

    def setup(self):
        pass

    def teardown(self):
        pass

    def test_mobile_phone_add(self):
        """ test mobile_phone to add """
        api = "mobile.phone.add"
        mobile_phone_info = json.dumps({
            'phone_number': "13822222222",
            'staff_id': 2,
            'mobile_devices_id': 2,
            'name': "张三",
            'identity': "123456789",
            'operator': "电信",
            'rent': "20元/月,用时一年",
            'tag': '',
            'remark': "",
            'status': "normal",
        })

        # result = self.access_api(api = api, staff_id = staff_id, mobile_info = mobile_info)
        result = self.access_api(api = api, mobile_phone_info = mobile_phone_info)


class Search(APITestCase):

    def setup(self):
        pass

    def teardown(self):
        pass

    def test_mobile_phone_search(self):
        """ test mobile_phone to search """
        api = "mobile.phone.search"
        current_page = 1
        search_info = json.dumps({

        })

        result = self.access_api(api = api, search_info = search_info,\
                                 current_page = current_page)
        self.assertTrue('data_list' in result)
        print(result["data_list"])

class Get(APITestCase):

    def setup(self):
        pass

    def teardown(self):
        pass

    def test_mobile_phone_get(self):
        """ test mobile_phone to get """
        api = "mobile.phone.get"
        mobile_phone_id = 1

        result = self.access_api(api = api, mobile_phone_id = mobile_phone_id)
        self.assertTrue('mobile_phone_info' in result)
        print(result["mobile_phone_info"])

class Update(APITestCase):

    def setup(self):
        pass

    def teardown(self):
        pass

    def test_mobile_phone_update(self):
        """ test mobile_phone to update """
        api = "mobile.phone.update"
        mobile_phone_id = 7
        mobile_phone_info = json.dumps({
            'phone_number': "13833333333",
            'staff_id': 2,
            'mobile_devices_id': 2,
            'name': "张三",
            'identity': "123456789",
            'operator': "电信",
            'rent': "20元/月,用时一年",
            'tag': '',
            'remark': "测试",
            'status': "normal",
        })
        result = self.access_api(api = api, mobile_phone_id = mobile_phone_id,
                                 mobile_phone_info = mobile_phone_info)

'''
class Remove(APITestCase):

    def setup(self):
        pass

    def teardown(self):
        pass

    def test_mobile_phone_remove(self):
        """ test mobile_phone to remove """
        api = "mobile.phone.remove"
        mobile_phone_id = 8
        result = self.access_api(api = api, mobile_phone_id = mobile_phone_id)
