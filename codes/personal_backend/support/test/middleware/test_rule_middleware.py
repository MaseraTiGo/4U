# coding=UTF-8

import unittest

from tuoen.abs.middleware.rule import rule_register


class RuleMiddleware(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_rule_mapping(self):
        """ test to get root rule"""
        rule_mapping = rule_register.get_rule_mapping()
        print(rule_mapping)
