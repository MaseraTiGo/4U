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
import urllib.request
import support.settings

# import thread package

# import my project package
from tuoen.sys.utils.common.signature import unique_parms, generate_signature


class APITestCase(unittest.TestCase):
    _test_url = "http://localhost:{}/interface/".format(support.settings.TEST_PORT)
    _auth_token = ""
    _renew_flag = ""

    def _get_current_time(self):
        return int(time.time())

    def _generate_signature(self, parms):
        unique_string, length = unique_parms(parms)
        return generate_signature(unique_string, length)

    def _get_api_url(self):
        return self._test_url

    def _combination_parms(self, **kwargs):
        parms = {
            "timestamp": self._get_current_time()
        }
        parms.update(kwargs)
        sign = self._generate_signature(parms)
        parms.update({"sign": sign})
        return parms

    def _connect(cls, url, data):
        postdata = urllib.parse.urlencode(data)
        postdata = postdata.encode('utf-8')
        result = ""
        with urllib.request.urlopen(url, postdata) as rep:
            result = rep.read().decode()
        return result

    def _parse(self, response_text):
        return json.loads(response_text)

    def _get_response_data(self, result):
        status = result['status']
        self.assertEqual(status, 'ok', result.get("msg", ""))
        return result['result']

    def _get_auth_token(self, flag='user'):
        api = "account.staff.login"
        username = "admin"  # "15623937796"#"13682286629"#
        password = "ddb41c840566d254f3d8e1b7ae1ab610"  # "650b94e46a745e4ac895db955f539e9d"
        result = self.access_base(flag=flag, api=api, username=username, \
                                  password=password)
        self._auth_token = result['auth_token']
        self._renew_flag = result['renew_flag']

    def access_api(self, api, flag='user', is_auth=True, **parms):
        if self._auth_token == "" and flag == 'user':
            self._get_auth_token()

        if is_auth:
            parms.update({'auth': self._auth_token})

        result = self.access_base(flag, api, **parms)
        return result

    def access_file_api(self, api, files=None, flag='file', is_auth=True, **parms):
        if self._auth_token == "":
            self._get_auth_token()

        if is_auth:
            parms.update({'auth': self._auth_token})

        access_parms = self._combination_parms(flag=flag, api=api, **parms)

        url = self._get_api_url()
        result = requests.post(url, data=access_parms, files=files)
        return self._get_response_data(result.json())

    def access_base(self, flag, api, **parms):
        access_parms = self._combination_parms(flag=flag, api=api, **parms)
        response_text = self._connect(self._get_api_url(), access_parms)
        result = self._parse(response_text)
        return self._get_response_data(result)
