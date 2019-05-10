# coding=UTF-8

import unittest

from tuoen.abs.service.task.crawler.zyw import ZYW
from tuoen.abs.service.task.crawler.ywg import YWG
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

    def test_zyw_crawler(self):
        zyw = ZYW()
        zyw.init()
        group = TaskGroup.query().order_by('-create_time')[0]
        zyw.run(group)


