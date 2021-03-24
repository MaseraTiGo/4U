# -*- coding: utf-8 -*-

# ===================================
# file_name     : search.py
# python_version: python 3.7.4
# file_author   : Johnathan.Strong
# create_time   : 2021/3/11 16:27
# ide_name      : PyCharm
# project_name  : 4U
# ===================================

import random


def binary_search(src_list, item):
    low = 0
    high = len(src_list) - 1
    while low <= high:
        mid = int((high - low) / 2) + low
        guess = src_list[mid]
        if guess > item:
            high = mid - 1
        elif guess < item:
            low = mid + 1
        else:
            return mid
    return None


# my_list = [1, 3, 5, 7, 9]
#
# print(binary_search(my_list, 7))


def my_binary_search(src_list: list, target: (str, int)) -> int:
    start_index = 0
    end_index = len(src_list) - 1
    while start_index <= end_index:
        mid_index = int((end_index + start_index) / 2)
        if src_list[mid_index] == target:
            return mid_index
        if src_list[mid_index] < target:
            start_index = mid_index + 1
        if src_list[mid_index] > target:
            end_index = mid_index
    print('target not in list')


my_fucking_list = list(range(10))
print(my_binary_search(my_fucking_list, 8))


def my_fucking_double_points_one(sorted_a: list, sorted_b: list):
    result = []
    a_index = b_index = 0
    while a_index <= len(sorted_a) - 1 and b_index <= len(sorted_b) - 1:
        a_item = sorted_a[a_index]
        b_item = sorted_b[b_index]
        if a_item < b_item:
            result.append(sorted_a[a_index])
            a_index += 1
        elif a_item > b_item:
            result.append(sorted_b[b_index])
            b_index += 1
        else:
            result.append(sorted_b[b_index])
            a_index += 1
            b_index += 1
        if a_index == len(sorted_a) and b_index < len(sorted_b):
            result.extend(sorted_b[b_index:])
        if b_index == len(sorted_b) and a_index < len(sorted_a):
            result.extend(sorted_a[a_index:])
    return result


# print(my_fucking_double_points_one([1, 3, 5, 7, 9], [2, 4, 6, 8, 10, 12]))


def my_fucking_double_points_two(sorted_a, sorted_b):
    result = []
    a_flag = b_flag = True
    while sorted_a or sorted_b:
        if a_flag:
            a_item = sorted_a.pop(0)
        if b_flag:
            b_item = sorted_b.pop(0)
        if a_item > b_item:
            result.append(b_item)
            a_flag, b_flag = False, True
        elif a_item == b_item:
            result.append(a_item)
            a_flag = b_flag = True
        else:
            result.append(a_item)
            a_flag, b_flag = True, False
        if not sorted_a and sorted_b:
            result.append(a_item)
            result.extend(sorted_b)
            break
        if not sorted_b and sorted_a:
            result.append(b_item)
            result.extend(sorted_a)
            break
    return result

# print(my_fucking_double_points_two([1, 3, 5, 7, 9], [2, 4, 6, 8, 10, 12]))
