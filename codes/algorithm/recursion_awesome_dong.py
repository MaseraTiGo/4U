# -*- coding: utf-8 -*-

# ===================================
# file_name     : recursion_awesome_dong.py
# python_version: python 3.7.4
# file_author   : Johnathan.Strong
# create_time   : 2021/5/3 19:54
# ide_name      : PyCharm
# project_name  : 4U
# ===================================

"""
                                      /
 __.  , , , _  _   __ ______  _    __/  __ ____  _,
(_/|_(_(_/_</_/_)_(_)/ / / <_</_  (_/_ (_)/ / <_(_)_
                                                 /|
                                                |/
"""


class ListNode:
    def __init__(self, val=0, next_=None):
        self.val = val
        self.next = next_


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


def iterate_list_node(list_node):
    while list_node:
        print(list_node.val, end="->")
        list_node = list_node.next


# ================================================= 21. Merge Two Sorted Lists==========================================

# Runtime: 32 ms, faster than 90.14% of Python3 online submissions for Merge Two Sorted Lists.
# Memory Usage: 14.3 MB, less than 31.59% of Python3 online submissions for Merge Two Sorted Lists.
class Solution21:
    def mergeTwoLists(self, l1: ListNode, l2: ListNode) -> ListNode:
        cur = root = ListNode()

        while l1 and l2:
            if l1.val <= l2.val:
                cur.next = cur = ListNode(l1.val)
                l1 = l1.next
            else:
                cur.next = cur = ListNode(l2.val)
                l2 = l2.next

        cur.next = l1 or l2
        return root.next


# iterate_list_node(Solution21().mergeTwoLists(GenList([1, 2, 4]).list_, GenList([1, 3, 4]).list_))


# ================================================= 21. Merge Two Sorted Lists==========================================


# ================================================= 1137. N-th Tribonacci Number========================================

# Runtime: 28 ms, faster than 77.35% of Python3 online submissions for N-th Tribonacci Number.
# Memory Usage: 14.3 MB, less than 43.12% of Python3 online submissions for N-th Tribonacci Number.
class Solution1137:
    def tribonacci(self, n: int) -> int:
        caching = [0, 1, 1]

        if n <= 2:
            return caching[n]
        for n in range(3, n + 1):
            temp = caching[0] + caching[1] + caching[2]
            caching = caching[1:] + [temp]

        return caching[-1]

    def tribonacci_dict(self, n: int) -> int:
        caching = {
            0: 0,
            1: 1,
            2: 1
        }

        if n in caching:
            return caching[n]
        for n in range(3, n + 1):
            caching[n] = caching[n - 3] + caching[n - 2] + caching[n - 1]

        return caching[n]


# print(Solution1137().tribonacci(25))
# ================================================= 1137. N-th Tribonacci Number========================================
