# coding=UTF-8

import json
import hashlib

from support.common.testcase.api_test_case import APITestCase


class TestAccount(APITestCase):

    # def test_account_login(self):
    #     api = 'account/login'
    #     username = 'black_deer'
    #     password = hashlib.md5("123456".encode('utf8')).hexdigest()
    #     result = self.access_api(api=api, flag='user', is_auth=False, username=username, password=password)
    #     print(result)

    # def test_account_change_passwd(self):
    #     api = 'account/changepassword'
    #     old_password = hashlib.md5("123456".encode('utf8')).hexdigest()
    #     new_password = hashlib.md5("000000".encode('utf8')).hexdigest()
    #     result = self.access_api(api=api, old_password=old_password, new_password=new_password)
    #     print(result)

    # def test_account_generate(self):
    #     api = 'account/generatesubaccount'
    #     account_info = json.dumps({
    #         'username': '008',
    #         'password': hashlib.md5("123456".encode('utf8')).hexdigest(),
    #         'name': 'venus',
    #         'phone': '13145201112',
    #         'role_id': 1,
    #         'status': 1
    #     })
    #     result = self.access_api(api=api, account_info=account_info)
    #     print(result)

    # def test_account_sub_list(self):
    #     api = 'account/subaccountlist'
    #     current_page = 1
    #     result = self.access_api(api=api, current_page=current_page)
    #     print('\n', result)

    # def test_account_status_reverse(self):
    #     api = 'account/statusreverse'
    #     account_id = 2
    #     result = self.access_api(api=api, account_id=account_id)
    #     print('\n', result)

    def test_account_update(self):
        api = 'account/updateaccount'
        account_id = 2
        update_info = {"username": "lu_01", "password": "e10adc3949ba59abbe56e057f20f883e", "name": "lu_01",
                       "phone": "15111221001", "role_id": 1, "stutas": "1"}
        result = self.access_api(api=api, account_id=account_id, update_info=update_info)
        print('\n', result)

    # def test_account_reset_passwd(self):
    #     api = 'account/resetpwd'
    #     account_id = 2
    #     result = self.access_api(api=api, account_id=account_id)
    #     print(result)

    # def test_account_delete(self):
    #     api = 'account/delete'
    #     account_id = 2
    #     result = self.access_api(api=api, account_id=account_id)
    #     print(result)

    # def test_account_edit(self):
    #     api = 'account/editaccount'
    #     update_info = json.dumps({
    #         'name': '橙鹿教育',
    #         'phone': '11111111111',
    #         'address': '湖北省武汉市',
    #     })
    #     result = self.access_api(
    #         api=api,
    #         update_info=update_info
    #     )
    #     print(result)

    ...
