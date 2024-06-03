# -*- coding: utf-8 -*-
# @File    : __init__.py
# @Project : 4U
# @Time    : 2024/5/27 16:10
# once, I want 2 leave my name 2 the history
# sadly, I find that my hair gets pale
"""                     
                                      /             
 __.  , , , _  _   __ ______  _    __/  __ ____  _, 
(_/|_(_(_/_</_/_)_(_)/ / / <_</_  (_/_ (_)/ / <_(_)_
                                                 /| 
                                                |/  
"""
import analysis.gprof2dot
from Interview.func import fucking_test


# select sort
def select_sort(data):
    if len(data) <= 1:
        return data

    for n in range(len(data) - 1):
        min_ = n
        for m in range(n + 1, len(data)):
            if data[min_] > data[m]:
                min_ = m
        if min_ != n:
            data[n], data[min_] = data[min_], data[n]
    return data


def insert_sort(data):
    if len(data) <= 1:
        return data

    for n in range(1, len(data)):
        for j in range(n):
            if data[n] < data[j]:
                tmp_val = data[n]
                data[j + 1:n + 1] = data[j:n]
                data[j] = tmp_val
    return data


def quick_sort(data):
    if len(data) <= 1:
        return data

    pivot = data[0]
    less_than_pivot = [x for x in data[1:] if x <= pivot]
    greater_than_pivot = [x for x in data[1:] if x > pivot]
    return quick_sort(less_than_pivot) + [pivot] + quick_sort(
        greater_than_pivot)


def merge_sort(arr):
    if len(arr) <= 1:
        return arr

    # Divide the array into two halves
    mid = len(arr) // 2
    left_half = arr[:mid]
    right_half = arr[mid:]

    # Recursively sort each half
    left_half = merge_sort(left_half)
    right_half = merge_sort(right_half)

    # Merge the sorted halves
    return merge(left_half, right_half)


def merge(left, right):
    merged = []
    left_idx, right_idx = 0, 0

    # Merge the two halves into a single sorted array
    while left_idx < len(left) and right_idx < len(right):
        if left[left_idx] < right[right_idx]:
            merged.append(left[left_idx])
            left_idx += 1
        else:
            merged.append(right[right_idx])
            right_idx += 1

    # Add any remaining elements from left and right halves
    merged.extend(left[left_idx:])
    merged.extend(right[right_idx:])

    return merged


def bubble_sort(data):
    if len(data) <= 1:
        return data

    for n in range(len(data) - 1):
        for m in range(len(data) - 1 - n):
            if data[m] > data[m + 1]:
                data[m], data[m + 1] = data[m + 1], data[m]
    return data


def binary_search(data, target):
    low = 0
    high = len(data) - 1

    while low <= high:
        mid = (low + high) // 2
        if data[mid] == target:
            return mid
        elif data[mid] < target:
            low = mid + 1
        else:
            high = mid - 1

    return -1



if __name__ == '__main__':
    # fucking_test(select_sort)
    # fucking_test(insert_sort)
    fucking_test(quick_sort)


