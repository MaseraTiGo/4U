# coding=UTF-8

import unittest

from tuoen.abs.service.account.manager import StaffAccountServer


class TestStaffAccountServer(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_staff_account_register(self):
        """ test register interface from account server """
        data_infos = [
            {
                'username': 'yrk',
                'ip': '192.168.3.249',
                'identity': '152127198907070012',
                'name': 'yangrongkai',
                'birthday': '1990-07-07',
                'phone': '15527703115',
                'gender': 'man',
                'email': '237818280@qq.com',
            },
            {
                'username': 'fsy',
                'ip': '192.168.3.44',
                'identity': '420684177711115455',
                'name': 'fengshiyu',
                'birthday': '1777-11-11',
                'phone': '14412314213',
                'gender': 'man',
                'email': '7718279@qq.com',
            },
        ]
        
        for data_info in data_infos:
            StaffAccountServer.register(**data_info)
    
    def test_staff_account_staff_login(self):
        """ test staff_login interface from account server """
        username = "fsy"
        password = "123456"
        StaffAccountServer.login(username,password)