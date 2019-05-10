# coding=UTF-8

import unittest

from tuoen.abs.middleware.department import department_middleware


class TestDepartmentMiddleware(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_get_root_department(self):
        """ test to get root department"""
        root = department_middleware.get_root()
        print(root.name, root.id)
        
    def test_get_children_department(self):
        """ test to get children department"""
        root = department_middleware.get_root()
        children = department_middleware.get_children(root.id)
        result = [(dp.name, dp.id) for dp in children]
        print(result)
    
    def test_get_all_children_department(self):
        """ test to get all children department"""
        root = department_middleware.get_root()
        children = department_middleware.get_all_children(root.id)
        result = [(dp.name, dp.id) for dp in children]
        print(result)
            
    def test_get_parent_department(self):
        """ test to get parent department"""
        root = department_middleware.get_root()
        children = department_middleware.get_all_children(root.id)
        department = children[-1]
        parent = department_middleware.get_parent(department.id)
        print(parent.name, parent.id)
        
    def test_get_parents_department(self):
        """ test to get parents department"""
        root = department_middleware.get_root()
        children = department_middleware.get_all_children(root.id)
        department = children[-1]
        parent_list = department_middleware.get_parents(department.id)
        for dp in parent_list:
            print(dp.name, dp.id)
            
    def test_tree(self):
        """test to get department tree"""
        root = department_middleware.get_root()
        tree_list = department_middleware.get_tree(root.id)
        print(tree_list)