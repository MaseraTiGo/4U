# coding=UTF-8

import json

from support.common.testcase.api_test_case import APITestCase


class Update(APITestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_equipment_register_update(self):
        """test equipment_register to update"""

        flag = "user"
        api = "equipment.register.update"
        quipment_register_id = 1
        quipment_register_info = json.dumps({
            "name" : "冯*",
            "phone": "138****4466"
        })

        result = self.access_api(flag = flag, api = api, quipment_register_id = quipment_register_id, \
                                 quipment_register_info = quipment_register_info)
