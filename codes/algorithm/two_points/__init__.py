# -*- coding: utf-8 -*-

# ===================================
# file_name     : __init__.py
# python_version: python 3.7.4
# file_author   : Johnathan.Strong
# create_time   : 2021/3/12 9:48
# ide_name      : PyCharm
# project_name  : 4U
# ===================================


from codes.algorithm.basics import MyNode

node_1 = MyNode(1)
node_2 = MyNode(2, node_1)
node_3 = MyNode(3, node_2)
node_4 = MyNode(4, node_3)
node_5 = MyNode(5, node_4)


# node_1._next = node_4


def ring_judge(node):
    node_f = node_s = node
    ring_flag = False
    while node_f and node_f.next:
        node_f = node_f.next.next
        node_s = node_s.next
        if node_f == node_s:
            print('have ring', node_f.value)
            ring_flag = True
            break

    if ring_flag:
        node_s = node
        while node_f != node_s:
            node_s = node_s.next
            node_f = node_f.next
        print(node_s, node_s.value)


# ring_judge(node_5)


def find_mid(node):
    slow_point = fast_point = node
    while fast_point.next:
        slow_point = slow_point.next
        fast_point = fast_point.next.next
    print(slow_point, slow_point.value)


# find_mid(node_5)

def find_last_k(node, last_index):
    slow_point = fast_point = node
    for _ in range(last_index - 1):
        fast_point = fast_point.next
    while fast_point.next:
        slow_point = slow_point.next
        fast_point = fast_point.next
    print(slow_point, slow_point.value)


# find_last_k(node_5, 3)

def find_target(sorted_list, target):
    s = 0
    e = len(sorted_list) - 1
    while s < e:
        sum_num = sorted_list[s] + sorted_list[e]
        if sum_num == target:
            return s, e
        elif sum_num > target:
            e -= 1
        else:
            s += 1
    return -1, -1


# print(find_target([1, 3, 5, 7, 9], 8))


# min substr


def find_min_substr(src_list: str, target: str):
    from collections import Counter
    res = src_list * 2
    p_head = p_tail = 0
    while p_head < len(src_list):
        temp_res = None
        temp = src_list[p_tail: p_head]
        keys = Counter(temp).keys()
        for item in target:
            if item not in keys:
                p_head += 1
                break
        else:
            not_break = True
            while not_break:
                p_tail += 1
                temp = src_list[p_tail: p_head]
                keys = Counter(temp).keys()
                for item in target:
                    if item not in keys:
                        not_break = False
                        break
            temp_res = src_list[p_tail - 1: p_head]
        if temp_res is not None:
            res = temp_res if len(temp_res) < len(res) else res
    return res


# print(find_min_substr('abbcdabcefg', 'bd'))


# 5. Longest Palindromic Substring
class Solution:
    def __init__(self, s: str):
        ...

    def longest_palindrome(self, s: str) -> str:
        if not s:
            return s
        pivot_h = pivot_t = 0


    def _helper(self, sub_str: str):
        ...

# 5. Longest Palindromic Substring
