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

    def test_mobile_maintain_add(self):
        """ test mobile_maintain to add """
        api = "mobile.maintain.add"
        mobile_maintain_info = json.dumps({
            'mobile_devices_id': 1,
            'staff_id': 2,
            'remark': "",
        })

        # result = self.access_api(api = api, staff_id = staff_id, mobile_info = mobile_info)
        result = self.access_api(api = api, mobile_maintain_info = mobile_maintain_info)


class Search(APITestCase):

    def setup(self):
        pass

    def teardown(self):
        pass

    def test_mobile_maintainsearch(self):
        """ test mobile_maintain to search """
        api = "mobile.maintain.search"
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

    def test_mobile_maintain_get(self):
        """ test mobile_maintain to get """
        api = "mobile.maintain.get"
        mobile_maintain_id = 11

        result = self.access_api(api = api, mobile_maintain_id = mobile_maintain_id)
        self.assertTrue('mobile_maintain_info' in result)
        print(result["mobile_maintain_info"])

class Update(APITestCase):

    def setup(self):
        pass

    def teardown(self):
        pass

    def test_mobile_maintain_update(self):
        """ test mobile_maintain to update """
        api = "mobile.maintain.update"
        mobile_maintain_id = 11
        mobile_maintain_info = json.dumps({
            'mobile_devices_id': 1,
            'staff_id': 2,
            'remark': "测试备注",
        })
        result = self.access_api(api = api, mobile_maintain_id = mobile_maintain_id,
                                 mobile_maintain_info = mobile_maintain_info)


class Remove(APITestCase):

    def setup(self):
        pass

    def teardown(self):
        pass

    def test_mobile_maintain_remove(self):
        """ test mobile_maintain to remove """
        api = "mobile.maintain.remove"
        mobile_maintain_id = 11
        result = self.access_api(api = api, mobile_maintain_id = mobile_maintain_id)

'''
