# coding=UTF-8

'''
Created on 2016年8月3日

@author: Administrator
'''

# import python standard package
import time
import json
import requests
import unittest
# import urllib.request
import support.test_settings

# import thread package

# import my project package
from tuoen.sys.utils.common.signature import unique_parms, generate_signature


class APITestCase(unittest.TestCase):
    _test_url = "http://localhost:{}/interface/".format(support.test_settings.TEST_PORT)
    _auth_token = ""
    _renew_flag = ""
    _headers = {"Content-Type": "application/json", "Accept": "*/*"}

    def _get_current_time(self):
        return int(time.time())

    def _generate_signature(self, parms):
        unique_string, length = unique_parms(parms)
        return generate_signature(unique_string, length)

    def _get_api_url(self):
        return self._test_url

    def _combination_parms(self, **kwargs):
        parms = {
            # "timestamp": self._get_current_time()
        }
        parms.update(kwargs)
        # sign = self._generate_signature(parms)
        # parms.update({"sign": sign})
        return parms

    def _connect(self, url, data):
        print(f'\nhandsome dong --------------> current url:\n {url} \n {data}')
        result = requests.post(url, data=json.dumps(data), headers=self._headers).json()
        return result

    def _parse(self, response_text):
        return json.loads(response_text)

    def _get_response_data(self, result):
        status = result['s']
        if status != '0':
            print('result--------------------->', result)
        self.assertEqual(status, '0', result.get("m", ""))
        return result['d']

    def _get_agent_auth_token(self):
        api = "account/login"
        username = "black_deer"  # "15623937796"#"13682286629"#
        password = "e10adc3949ba59abbe56e057f20f883e"  # "650b94e46a745e4ac895db955f539e9d"
        result = self.access_base(flag='user', api=api, username=username, password=password)
        self._auth_token = result['auth_token']

    def _get_platform_auth_token(self):
        api = "account/login"
        username = "black_deer"
        password = "e10adc3949ba59abbe56e057f20f883e"
        result = self.access_base(flag='admin', api=api, username=username, password=password)
        self._auth_token = result['auth_token']

    def access_api(self, api, flag='user', is_auth=True, **parms):
        if self._auth_token == "" and is_auth:
            if flag == 'user':
                self._get_agent_auth_token()
            elif flag == 'admin':
                self._get_platform_auth_token()

        if is_auth:
            self._headers.update({'Authorization': self._auth_token})
        result = self.access_base(flag, api, **parms)
        return result

    def access_file_api(self, api, files=None, flag='file', is_auth=True, **parms):
        if self._auth_token == "":
            self._get_auth_token()

        if is_auth:
            parms.update({'token': self._auth_token})

        access_parms = self._combination_parms(flag=flag, **parms)

        url = self._get_api_url()
        result = requests.post(url, data=access_parms, files=files)
        return self._get_response_data(result.json())

    def access_base(self, flag, api, **parms):
        access_parms = self._combination_parms(flag=flag, **parms)
        response_text = self._connect(self._get_api_url() + api, access_parms)
        return self._get_response_data(response_text)
