# coding=UTF-8

import unittest

from tuoen.abs.service.task.crawler.qcc import QCC
from model.store.model_task import TaskGroup


class TestCrawlerServer(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_ywg_crawler(self):
        """ test ywg crawler """
        ywg = YWG()
        ywg.init()
        group = TaskGroup.query().order_by('-create_time')[0]
        ywg.run(group)
