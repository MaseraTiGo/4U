# -*- coding: utf-8 -*-
# @File    : tree
# @Project : 4U
# @Time    : 2024/5/29 14:42
# once, I want 2 leave my name 2 the history
# sadly, I find that my hair gets pale
"""                     
                                      /             
 __.  , , , _  _   __ ______  _    __/  __ ____  _, 
(_/|_(_(_/_</_/_)_(_)/ / / <_</_  (_/_ (_)/ / <_(_)_
                                                 /| 
                                                |/  
"""
from Interview.func import construct_binary_tree, gen_random_list


def dfs(root):
    if root is not None:
        yield from dfs(root.left)
        yield root.value
        yield from dfs(root.right)


def bfs(root):
    if root is not None:
        queue = [root]
        while queue:
            node = queue.pop(0)
            yield node.value
            queue.extend([i for i in (node.left, node.right) if i is not None])


if __name__ == '__main__':
    tree = construct_binary_tree(gen_random_list())
    print(list(dfs(tree)))
    print(list(bfs(tree)))
