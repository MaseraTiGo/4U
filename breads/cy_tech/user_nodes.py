# -*- coding: utf-8 -*-
# @File    : user_nodes
# @Project : 4U
# @Time    : 2024/8/17 9:21
# once, I want 2 leave my name 2 the history
# sadly, I find that my hair gets pale
"""                     
                                      /             
 __.  , , , _  _   __ ______  _    __/  __ ____  _, 
(_/|_(_(_/_</_/_)_(_)/ / / <_</_  (_/_ (_)/ / <_(_)_
                                                 /| 
                                                |/  
"""
from copy import deepcopy

# -*- coding: utf-8 -*-
# @File    : __init__.py
# @Project : ez_web
# @Time    : 2023/9/11 16:18
# once, I want 2 leave my name 2 the history
# sadly, I find that my hair gets pale
"""                     
                                      /             
 __.  , , , _  _   __ ______  _    __/  __ ____  _, 
(_/|_(_(_/_</_/_)_(_)/ / / <_</_  (_/_ (_)/ / <_(_)_
                                                 /| 
                                                |/  
"""


class X:
    def __init__(self, id=None, children=None):
        self.id = id
        self.children = children


class Node:
    def __init__(self, id_, children=None):
        self.id = id_
        self.children = children if children else []


def fucking_tree(qs, p_node):
    if not qs:
        return
    for obj in qs:
        cur_node = Node(obj.id)
        p_node.children.append(cur_node)
        fucking_tree(obj.children, cur_node)


def traversal(root_):
    temp = []

    path = []

    def dfs_helper(node):
        if node:
            path.append(node.id)
            print(f"current node is:{node.id}--{path}")
            if not node.children:
                yield deepcopy(path)

            for child in node.children:
                yield from dfs_helper(child)
            path.pop()

    print(list(dfs_helper(root_)))
    return temp


if __name__ == '__main__':
    root = Node(0)

    node_1, node_2, node_3, node_4, node_5, node_6, node_7, node_8, node_9, node_10 = [
        X(i) for i in range(1, 11)]
    node_11, node_12, node_13, node_14 = [X(i) for i in range(11, 15)]

    node_1.children = [node_2, node_3, node_4, node_5]
    node_3.children = [node_6, node_7]
    node_4.children = [node_8]
    node_5.children = [node_9, node_10]
    node_7.children = [node_11]
    node_8.children = [node_12]
    node_9.children = [node_13]
    node_11.children = [node_14]
    # data = ...
    fucking_tree(node_1.children, root)
    print(traversal(root))
