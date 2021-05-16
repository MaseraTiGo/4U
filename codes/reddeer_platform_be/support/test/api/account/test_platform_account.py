# coding=UTF-8
import json
import hashlib
from support.common.testcase.api_test_case import APITestCase


class TestAccount(APITestCase):
    _flag = "admin"

    # def test_account_generateagentaccount(self):
    #     api = 'account/generateagentaccount'
    #     account_info = json.dumps({
    #         'username': "lulaji",
    #         'password': hashlib.md5("123456".encode('utf8')).hexdigest(),
    #         'name': '鲁垃圾',
    #         'phone': '11111222222',
    #         'company_name': '垃圾搬运有限公司',
    #         'company_phone': '11133333333',
    #         'company_address': '垃圾厂',
    #         'status': 1,
    #     })
    #     result = self.access_api(
    #         api=api, flag=self._flag,
    #         account_info=account_info
    #     )
    #     print(result)

    # def test_account_agentaccountlist(self):
    #     api = 'account/agentaccountlist'
    #     current_page = 1
    #     query_info = json.dumps({
    #     })
    #     result = self.access_api(
    #         api=api, flag=self._flag,
    #         current_page=current_page,
    #         query_info=query_info,
    #     )
    #     print(result)

    # def test_account_statusreverse(self):
    #     api = 'account/statusreverse'
    #     account_id = 1
    #     result = self.access_api(
    #         api=api, flag=self._flag,
    #         account_id=account_id
    #     )
    #     print(result)

    # def test_account_delete(self):
    #     api = 'account/delete'
    #     account_id = 1
    #     result = self.access_api(
    #         api=api, flag=self._flag,
    #         account_id=account_id
    #     )
    #     print(result)

    # def test_account_resetagentpwd(self):
    #     api = 'account/resetagentpwd'
    #     account_id = 1
    #     result = self.access_api(
    #         api=api, flag=self._flag,
    #         account_id=account_id
    #     )
    #     print(result)

    # def test_account_resetagentpwd(self):
    #     api = 'account/editagentaccount'
    #     account_id = 1
    #     edit_info = json.dumps({
    #         'username': "lulaji002",
    #         'password': hashlib.md5("123456".encode('utf8')).hexdigest(),
    #         'name': '鲁垃圾',
    #         'phone': '11111222222',
    #         'company_name': '垃圾搬运有限公司2',
    #         'company_phone': '11133333333',
    #         'company_address': '垃圾厂',
    #         'status': 0,
    #     })
    #     result = self.access_api(
    #         api=api, flag=self._flag,
    #         account_id=account_id,
    #         edit_info=edit_info
    #     )
    #     print(result)
