# -*- coding: utf-8 -*-
# @File    : recursion_awesome_dong.py
# @Project : 4U
# @Time    : 2021/5/6 9:32
"""
                                      /
 __.  , , , _  _   __ ______  _    __/  __ ____  _,
(_/|_(_(_/_</_/_)_(_)/ / / <_</_  (_/_ (_)/ / <_(_)_
                                                 /|
                                                |/
"""


# ========================================== public area ===== =========================================================

# Definition for a binary tree node.
class TreeNode:
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None


# ========================================== public area ===== =========================================================


# ======================================= 1379. Find a Corresponding Node of a Binary Tree in a Clone of That Tree =====
# Runtime: 604 ms, faster than 92.47% of Python3 online submissions for Find a Corresponding Node of a Binary Tree in
# a Clone of That Tree.
# Memory Usage: 24.2 MB, less than 52.71% of Python3 online submissions for Find a Corresponding Node of a Binary Tree
# in a Clone of That Tree.


class Solution1379:
    def getTargetCopy(self, original: TreeNode, cloned: TreeNode, target: TreeNode) -> TreeNode:
        l_node = [cloned]
        while l_node:
            for node in l_node:
                if node.val == target.val:
                    return node
            l_node = [leaf for node in l_node for leaf in (node.left, node.right) if leaf]

        return None


# ======================================= 1379. Find a Corresponding Node of a Binary Tree in a Clone of That Tree =====


# ======================================= 1780. Check if Number is a Sum of Powers of Three ============================

# Runtime: 32 ms, faster than 72.98% of Python3 online submissions for Check if Number is a Sum of Powers of Three.
# Memory Usage: 14.4 MB, less than 22.30% of Python3 online submissions for Check if Number is a Sum of Powers of Three.
class Solution1780:
    def checkPowersOfThree(self, n: int) -> bool:
        while n > 0:
            n, res = divmod(n, 3)
            if res != 0 and res != 1:
                return False

        return True


print(Solution1780().checkPowersOfThree(91))
# ======================================= 1780. Check if Number is a Sum of Powers of Three ============================
