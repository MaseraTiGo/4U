# coding=UTF-8

import json

from support.common.testcase.api_test_case import APITestCase


class TransferPosition(APITestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_uset_staff_getbyadmin(self):
        """test user staff to transfer position"""
        staff_id = 33
        input_info = json.dumps({
            'transfer_time': '2017-07-20 00:00:00',
            'desc_dept': 33
        })
        flag = "user"
        api = "user.staff.positiontransfer"

        self.access_api(flag=flag, api=api, staff_id=staff_id, input_info=input_info)


'''
class Add(APITestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_user_staff_add(self):
        """test user satff to add"""

        flag = "user"
        api = "user.staff.add"
        user_info = json.dumps({
            'name': "冯时宇",
            'birthday': "2018-04-16",
            'phone': "15232626262",
            'email': "2058556456@qq.com",
            'gender': "man",
            'number': "007",
            'identity': "123456789",
            'emergency_contact': "风小炎",
            'emergency_phone': "13562525452",
            'address': "湖北省武汉市江夏区",
            'entry_time': "2017-3-13",
            'education': "大学本科",
            'bank_number': "6440 2121 0212 4545",
            'contract_b': "02345644461",
            'contract_l': "05864654564",
            'expire_time': "2018-3-13",
            'role_ids' :[1],
            'department_ids' :[1],
        })

        result = self.access_api(flag = flag, api = api, user_info = user_info)

class Getbyadmin(APITestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_uset_staff_getbyadmin(self):
        """test user staff to getbyadmin"""

        flag = "user"
        api = "user.staff.getbyadmin"
        user_id = 33

        result = self.access_api(flag = flag, api = api, user_id = user_id)
        print(result["user_info"])
        self.assertTrue('user_info' in result)

class Updatebyadmin(APITestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_user_staff_UpdateByAdmin(self):
        """ test user satff to UpdateByAdmin"""

        flag = "user"
        api = "user.staff.updatebyadmin"
        user_id = 33
        user_info = json.dumps({
            'name': "冯时宇",
            'birthday': "2018-04-16",
            'phone': "15232626262",
            'email': "2058556456@qq.com",
            'gender': "man",
            'number': "007",
            'identity': "123456789",
            'emergency_contact': "风炎",
            'emergency_phone': "13562525452",
            'address': "湖北省武汉市江夏区",
            'entry_time': "2017-3-13",
            'education': "大学本科",
            'bank_number': "6440 2121 0212 4545",
            'contract_b': "02345644461",
            'contract_l': "05864654564",
            'expire_time': "2018-3-13",
            'role_ids' :[1],
            'department_ids' :[1],
        })

        result = self.access_api(flag = flag, api = api, user_id = user_id, user_info = user_info)

class Get(APITestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_user_staff_get(self):
        """test user satff to get"""

        flag = "user"
        api = "user.staff.get"

        result = self.access_api(flag = flag, api = api)
        self.assertTrue('user_info' in result)

class Search(APITestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_user_staff_search(self):
        """test user staff to search"""

        flag = "user"
        api = "user.staff.search"
        current_page = 1
        search_info = json.dumps({

        })

        result = self.access_api(flag = flag, api = api, current_page = current_page, search_info = search_info)
        print(result["data_list"])
        self.assertTrue('data_list' in result)


class Roster(APITestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_user_staff_search(self):
        """test user staff to roster"""

        flag = "user"
        api = "user.staff.roster"
        current_page = 1
        search_info = json.dumps({

        })

        result = self.access_api(flag = flag, api = api, current_page = current_page, search_info = search_info)
        print(result["data_list"])
        self.assertTrue('data_list' in result)


class SearchAll(APITestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_user_staff_searchall(self):
        """test user staff to searchall"""

        flag = "user"
        api = "user.staff.searchall"
        search_info = json.dumps({

        })

        result = self.access_api(flag = flag, api = api, search_info = search_info)
        print(result["data_list"])
        self.assertTrue('data_list' in result)
        print(result["data_list"])

class  Update(APITestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_user_staff_update(self):
        """test user to update"""

        flag = "user"
        api = "user.staff.update"
        user_info = json.dumps({
            'name': "yrk",
            'birthday': "1969-12-13",
            'phone': "13888888888",
            'email': "2058556456@qq.com",
            'gender': "man",
            'number': "008",
        })

        result = self.access_api(flag = flag, api = api, user_info = user_info)
'''
