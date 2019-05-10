# coding=UTF-8

import json

from support.common.testcase.api_test_case import APITestCase

# class Search(APITestCase):
#
#     def setUp(self):
#         pass
#
#     def tearDown(self):
#         pass
#
#     def test_order_search(self):
#         """test order to search"""
#
#         flag = "user"
#         api = "order.returns.search"#"service_item_search"#
#         current_page = 1
#         search_info = json.dumps({
#         })
#
#         result = self.access_api(flag = flag, api = api, current_page = current_page, search_info = search_info)
#         self.assertTrue('data_list' in result)
#         print(result["data_list"])

'''
class Get(APITestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_order_get(self):
        """test order to get"""

        flag = "user"
        api = "order.get"
        order_id = 1

        result = self.access_api(flag = flag, api = api, order_id = order_id)
        self.assertTrue('order_info' in result)
        print(result["order_info"])



class Get(APITestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_order_search(self):
        """test order to get"""

        flag = "user"
        api = "order.returns.get"#"service_item_search"#
        #current_page = 1
        search_info = json.dumps({

        })
        order_id = 7516
        result = self.access_api(flag = flag, api = api, order_id=order_id)
        #self.assertTrue('data_list' in result)
        print(result)

class Update(APITestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_order_search(self):
        """test order to update"""

        flag = "user"
        api = "order.returns.update"#"service_item_search"#
        #current_page = 1
        update_info = json.dumps({
            'id': 7516,
            'code': '121212121212',
            'customer': 'dongjundong',
        })
        #order_id = 7516
        result = self.access_api(flag = flag, api = api, update_info=update_info)
        #self.assertTrue('data_list' in result)
        print(result)

class Change(APITestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_order_change(self):
        """test order to change"""

        flag = "user"
        api = "order.returns.change"#"service_item_search"#
        #current_page = 1
        update_info = json.dumps({
            'flag': 2,
            'code': '720300010973102',
        })
        #order_id = 7516
        result = self.access_api(flag = flag, api = api, change_info=update_info)
        #self.assertTrue('data_list' in result)
        print(result)
'''
# class Remove(APITestCase):
#
#     def setUp(self):
#         pass
#
#     def tearDown(self):
#         pass
#
#     def test_order_remove(self):
#         """test order to remove"""
#
#         flag = "user"
#         api = "order.returns.remove"#"service_item_search"#
#         #current_page = 1
#         update_info = json.dumps({
#             'code': '730300010036654',
#         })
#         #order_id = 7516
#         result = self.access_api(flag = flag, api = api, remove_info=update_info)
#         #self.assertTrue('data_list' in result)
#         print(result)
    #
    # def test_order_returns(self):
    #     """test order to add"""
    #
    #     flag = "user"
    #     api = "order.returns.add"#"service_item_search"#
    #     #current_page = 1
    #     returns_info = json.dumps({
    #         'code': '0000730300010036654',
    #     })
    #     #order_id = 7516
    #     result = self.access_api(flag = flag, api = api, returns_info=returns_info)
    #     #self.assertTrue('data_list' in result)
    #     print(result)

    # def test_order_returns(self):
    #     """test order to Get detail"""
    #
    #     flag = "user"
    #     api = "order.returns.get"#"service_item_search"#
    #     #current_page = 1
    #     order_id = 3
    #     result = self.access_api(flag = flag, api = api, order_id=order_id)
    #     #self.assertTrue('data_list' in result)
    #     print(result)
class Recover(APITestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_order_returns(self):
        """test order to recover"""

        flag = "user"
        api = "order.returns.recover"#"service_item_search"#
        #current_page = 1
        recover_info = json.dumps({
            'code': '730300010036654',
        })
        #order_id = 7516
        result = self.access_api(flag = flag, api = api, recover_info=recover_info)
        #self.assertTrue('data_list' in result)
        print(result)
