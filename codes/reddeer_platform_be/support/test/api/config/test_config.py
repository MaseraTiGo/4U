# coding=UTF-8
import json

from support.common.testcase.api_test_case import APITestCase


class TestConfig(APITestCase):
    def test_notice_search(self):
        flag = "user"
        api = "notice.search"
        current_page = 1
        search_info = json.dumps({})
        result = self.access_api(flag=flag, api=api, current_page=current_page, search_info=search_info)
        assert 'data_list' in result

    def test_notice_add(self):
        flag = "user"
        api = "notice.add"
        notice_info = json.dumps({
            'type': 'notice',
            'content': 'just a test',
            'is_use': True,
            'platform': 'crm'
        })
        self.access_api(flag=flag, api=api, notice_info=notice_info)

    def test_notice_update(self):
        flag = "user"
        api = "notice.update"
        notice_id = 1
        notice_info = json.dumps({
            'type': 'notice',
            'content': 'just a test by updating',
            'is_use': True,
            'platform': 'crm'
        })
        self.access_api(flag=flag, api=api, notice_id=notice_id, notice_info=notice_info)

    def test_notice_remove(self):
        flag = "user"
        api = "notice.remove"
        notice_id = 1
        self.access_api(flag=flag, api=api, notice_id=notice_id)

    def test_notice_staff_search(self):
        flag = "user"
        api = "notice.staffsearch"
        search_info = json.dumps({})

        result = self.access_api(flag=flag, api=api, search_info=search_info)
        assert 'data_list' in result
