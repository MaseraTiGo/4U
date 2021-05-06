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


# Definition for singly-linked list.
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


class GenList(object):
    def __init__(self, values):
        if not isinstance(values, (list, tuple)):
            raise Exception('give me fucking right type ok?')
        if not values:
            raise Exception('it is fucking empty')
        self.values = values

    @property
    def list_(self):
        root_ = ListNode(self.values[0])
        src = root_
        len_ = len(self.values)

        for i in range(1, len_):
            curr = ListNode(self.values[i])
            root_.next = curr
            root_ = root_.next
        return src


# ========================================== public area ===== =========================================================


# ======================================= 24. Swap Nodes in Pairs ======================================================

# Runtime: 24 ms, faster than 95.37% of Python3 online submissions for Swap Nodes in Pairs.
# Memory Usage: 14.4 MB, less than 16.10% of Python3 online submissions for Swap Nodes in Pairs.
class Solution24:
    def swapPairs_self(self, head: ListNode) -> ListNode:
        if not head or not head.next:
            return head
        list_vars = []
        while head:
            list_vars.append(head.val)
            head = head.next
        from math import ceil
        root = head = ListNode(-1)
        for i in range(ceil((len(list_vars) / 2))):
            for item in list_vars[2 * i: 2 * (i + 1)][::-1]:
                root.next = root = ListNode(item)
        return head.next

    def swapPairs(self, head: ListNode) -> ListNode:
        p1 = head
        p2 = head.next if head else None

        while p1 and p2:
            p1.val, p2.val = p2.val, p1.val
            p1 = p2.next
            p2 = p1.next if p1 else None
        return head


# rs = Solution24().swapPairs(GenList([1, 2, 3, 4]).list_)
# while rs:
#     print(rs.val, end="->")
#     rs = rs.next


# ======================================= 24. Swap Nodes in Pairs ======================================================


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

# print(Solution1780().checkPowersOfThree(91))
# ======================================= 1780. Check if Number is a Sum of Powers of Three ============================
