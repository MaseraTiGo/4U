# coding=UTF-8

import unittest

from tuoen.abs.middleware.role import role_middleware


class TestRoleMiddleware(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_get_root_role(self):
        """ test to get root role"""
        root = role_middleware.get_root()
        print(root.name, root.id)

    def test_get_children_role(self):
        """ test to get children role"""
        root = role_middleware.get_root()
        children = role_middleware.get_children(root.id)
        result = [(ro.name, ro.id) for ro in children]
        print(result)

    def test_get_all_children_role(self):
        """ test to get all children role"""
        root = role_middleware.get_root()
        children = role_middleware.get_all_children(root.id)
        result = [(ro.name, ro.id) for ro in children]
        print(result)

    def test_get_parent_role(self):
        """ test to get parent role"""
        root = role_middleware.get_root()
        children = role_middleware.get_all_children(root.id)
        role = children[-1]
        parent = role_middleware.get_parent(role.id)
        print(parent.name, parent.id)

    def test_get_parents_role(self):
        """ test to get parents role"""
        root = role_middleware.get_root()
        children = role_middleware.get_all_children(root.id)
        role = children[-1]
        parent_list = role_middleware.get_parents(role.id)
        for ro in parent_list:
            print(ro.name, ro.id)

    def test_tree(self):
        """test to get role tree"""
        root = role_middleware.get_root()
        tree_list = role_middleware.get_tree(root.id)
        role_middleware.force_refresh()
        print(tree_list)
