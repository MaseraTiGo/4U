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

from typing import List


# ========================================== public area ===== =========================================================

# Definition for a binary tree node.
class TreeNode:
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None


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


# ======================================= 779. K-th Symbol in Grammar ==================================================
from math import log2


# todo: dong not understand.
class Solution779:
    def kthGrammar(self, N: int, K: int) -> int:
        if K <= 2:
            return abs(K - 1)

        u = 1 << int(log2(K - 1))

        return 1 - self.kthGrammar(N - 1, K - u)


# print(Solution779().kthGrammar(30, 434991989))


# ======================================= 779. K-th Symbol in Grammar ==================================================

# ======================================= 967. Numbers With Same Consecutive Differences ===============================

class Solution967:
    def numsSameConsecDiff(self, n: int, k: int) -> List[int]:
        ans = []

        for j in range(1, 10):
            temp = [str(j)]
            for _ in range(n):
                temp_2 = []
                for item in temp:
                    i = int(item[-1])
                    if i - k >= 0:
                        temp_2.append(item + str(i - k))
                    if i + k < 10:
                        num = item + str(i + k)
                        if num not in temp_2:
                            temp_2.append(num)
                temp = temp_2
            ans.extend(temp)

        return list(set([int(item) for item in ans]))


print(Solution967().numsSameConsecDiff(2, 0))


# ======================================= 967. Numbers With Same Consecutive Differences ===============================


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
