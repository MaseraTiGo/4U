# coding=UTF-8

import unittest

from tuoen.abs.service.journal.manager import StaffJournalServer


class TestJournalServer(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_journal_select(self):
        """ test select interface from journal server """
        StaffJournalServer.search()
