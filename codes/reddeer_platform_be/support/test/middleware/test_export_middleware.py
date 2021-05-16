# coding=UTF-8

import unittest
from model.store.model_department import Department
from tuoen.abs.middleware.export.department_demo import department_export_middleware


class ExportMiddleware(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_export(self):
        print("===export")
        # department_qs = Department.search()
        print("===>1111111111111")
        result = department_export_middleware.run(None)
        print("======result", result)
