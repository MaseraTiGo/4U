# -*- coding: utf-8 -*-
# @File    : func
# @Project : 4U
# @Time    : 2024/5/28 9:46
# once, I want 2 leave my name 2 the history
# sadly, I find that my hair gets pale
"""                     
                                      /             
 __.  , , , _  _   __ ______  _    __/  __ ____  _, 
(_/|_(_(_/_</_/_)_(_)/ / / <_</_  (_/_ (_)/ / <_(_)_
                                                 /| 
                                                |/  
"""
import random


def fucking_test(sort_algorithm, test_times=5):
    print(f"{sort_algorithm.__name__:=^88}")
    test_data = list(range(10))
    for _ in range(test_times):
        print(f"{_:*^66}")
        shuffled_list = test_data[:]
        random.shuffle(shuffled_list)
        print(f"loop {_} test data: {shuffled_list}")
        assert sort_algorithm(shuffled_list) == test_data
        print(f"test loop {_} passed!")
        print(f"{_:*^66}")
        print()
    print(f"well done, everything is fine!")
    print(f"{sort_algorithm.__name__:=^88}")
    print()


def gen_random_list(start=0, end=100, length=10):
    ret = [random.randint(start, end) for _ in range(length)]
    print(f"random list is ->: {ret}")
    return ret


class TreeNode:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None


def insert_level_order(arr, i, n):
    if i < n:
        temp = TreeNode(arr[i])

        temp.left = insert_level_order(arr, 2 * i + 1, n)

        temp.right = insert_level_order(arr, 2 * i + 2, n)

        return temp

    return None


def construct_binary_tree(arr):
    if not arr:
        return None

    return insert_level_order(arr, 0, len(arr))