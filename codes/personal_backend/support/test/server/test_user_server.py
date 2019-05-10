# coding=UTF-8

import unittest

from tuoen.service.user.manager import UserServer


class TestUserServer(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_user_login(self):
        """ test login interface from user server """
        account, password = "yangrongkai", "123456"
        user, token = UserServer.login(account, password)

