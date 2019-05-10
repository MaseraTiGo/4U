# coding=UTF-8

import json

from support.common.testcase.api_test_case import APITestCase

'''
class Add(APITestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass
    

    def test_mobile_devices_add(self):
        """test mobile_devices to add"""
        
        flag = "user"
        api = "mobile.devices.add"
        mobile_devices_info = json.dumps({
            'code': "0011",
            'brand': "三星",
            'model': "XXX",
            'price': 1000000,
            'status': "normal",
            'remark': "",
        })
        
        result = self.access_api(flag = flag, api = api, mobile_devices_info = mobile_devices_info)

class Search(APITestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_mobile_devices_search(self):
        """ test mobile_devices Search """

        flag = "user"
        api = "mobile.devices.search"
        current_page = 1
        search_info = json.dumps({

        })

        result = self.access_api(flag = flag, api = api, current_page = current_page, search_info = search_info)
        print(result["data_list"])
        self.assertTrue('data_list' in result)

'''
class Searchall(APITestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_mobile_devices_searchall(self):
        """ test mobile_devices searchall """

        flag = "user"
        api = "mobile.devices.searchall"
        search_info = json.dumps({

        })

        result = self.access_api(flag = flag, api = api, search_info = search_info)
        print(result["data_list"])
        self.assertTrue('data_list' in result)

'''
class Get(APITestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_mobile_devices_get(self):
        """test mobile_devices to get"""
        
        flag = "user"
        api = "mobile.devices.get"
        mobile_devices_id = 1
        
        result = self.access_api(flag = flag, api = api, mobile_devices_id = mobile_devices_id)
        print(result["mobile_devices_info"])
        self.assertTrue('mobile_devices_info' in result)
        
    
class Update(APITestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_mobile_devices_update(self):
        """test mobile_devices update"""
        
        flag = "user"
        api = "mobile.devices.update"
        mobile_devices_id = 11
        mobile_devices_info = json.dumps({
            'code': "0011",
            'brand': "三星",
            'model': "XXX",
            'price': 1000000,
            'status': "normal",
            'remark': "测试备注",
        })
        
        result = self.access_api(flag = flag, api = api, mobile_devices_id = mobile_devices_id, \
                                 mobile_devices_info = mobile_devices_info)
    

class Remove(APITestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_mobile_devices_remove(self):
        """test mobile_devices to remove"""
        
        flag = "user"
        api = "mobile.devices.remove"
        mobile_devices_id = 11
        
        result = self.access_api(flag = flag, api = api, mobile_devices_id = mobile_devices_id)

'''
