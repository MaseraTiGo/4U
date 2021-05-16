# coding=UTF-8

import json

from support.common.testcase.api_test_case import APITestCase


class TestRole(APITestCase):
    # def test_role_list(self):
    #     api = 'role/list'
    #     current_page = 1
    #     result = self.access_api(api=api, current_page=current_page)
    #     print('\n', result)

    # def test_role_status_reverse(self):
    #     api = 'role/statusreverse'
    #     role_id = 2
    #     result = self.access_api(api=api, role_id=role_id)
    #     print('\n', result)

    # def test_role_delete(self):
    #     api = 'role/delete'
    #     role_id = 3
    #     result = self.access_api(api=api, role_id=role_id)
    #     print('\n', result)

    def test_role_edit(self):
        api = 'role/edit'
        role_id = 3
        edit_info = json.dumps({
            'name': 'admin',
            'rules': json.dumps(['role/edit']),
            'status': 1
        })
        result = self.access_api(api=api, role_id=role_id, edit_info=edit_info)
        print('\n', result)

    # def test_role_create(self):
    #     api = 'role/create'
    #     create_info = json.dumps({
    #         'name': '你好',
    #         'rules': json.dumps([]),
    #         'status': 1
    #     })
    #     result = self.access_api(api=api, create_info=create_info)
    #     print('\n', result)
    ...
