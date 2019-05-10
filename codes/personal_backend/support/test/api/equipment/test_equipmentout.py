# coding=UTF-8

import json

from support.common.testcase.api_test_case import APITestCase


class Update(APITestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    # def test_equipment_register_search(self):
    #     """test equipment_register to update"""
    #
    #     flag = "user"
    #     api = "equipment.equipmentout.search"
    #     current_page = 1
    #     search_info = json.dumps({
    #     })
    #
    #     result = self.access_api(flag = flag, api = api, current_page = current_page, \
    #                              search_info = search_info)
    #     self.assertTrue('data_list' in result)
    #     print('====================>', result['data_list'])

    def test_equipment_register_update(self):
        """test equipment_out to update"""

        flag = "user"
        api = "equipment.equipmentout.update"
        eo_id = 1
        eo_info = json.dumps({
            'remark': "測試更新,更新remark",
        })

        result = self.access_api(flag = flag, api = api, eo_id = eo_id, \
                                 eo_info = eo_info)
        print('====================>', result)
        self.assertTrue(result is None)