# coding=UTF-8

import json

from support.common.testcase.api_test_case import APITestCase


class Update(APITestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_equipment_register_search(self):
        """test equipment_register to update"""

        flag = "user"
        api = "equipment.equipmentin.search"
        current_page = 1
        search_info = json.dumps({
        })

        result = self.access_api(flag = flag, api = api, current_page = current_page, \
                                 search_info = search_info)
        self.assertTrue('data_list' in result)
        print('====================>', result['data_list'])

    # def test_equipment_register_update(self):
    #     """test equipment_in to update"""
    #
    #     flag = "user"
    #     api = "equipment.equipmentin.update"
    #     ei_id = 1
    #     ei_info = json.dumps({
    #         'remark': "測試更新,測試操作類型是否正確",
    #     })
    #
    #     result = self.access_api(flag = flag, api = api, ei_id = ei_id, \
    #                              ei_info = ei_info)
    #     print('====================>', result)
    #     self.assertTrue(result is None)
