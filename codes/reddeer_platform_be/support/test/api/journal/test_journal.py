# coding=UTF-8
import json

from support.common.testcase.api_test_case import APITestCase


class TestJournal(APITestCase):
    def test_journal_search(self):
        flag = "user"
        api = "journal.search"
        search_info = {}
        result = self.access_api(flag=flag, api=api, search_info=json.dumps(search_info))
        assert 'data_list' in result
