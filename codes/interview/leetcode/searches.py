# -*- coding: utf-8 -*-
# @File    : searches
# @Project : 4U
# @Time    : 2024/5/24 14:42
# once, I want 2 leave my name 2 the history
# sadly, I find that my hair gets pale
"""                     
                                      /             
 __.  , , , _  _   __ ______  _    __/  __ ____  _, 
(_/|_(_(_/_</_/_)_(_)/ / / <_</_  (_/_ (_)/ / <_(_)_
                                                 /| 
                                                |/  
"""
from typing import List


def binary_search(data: List[int], target=None):
    if not data or target is None:
        return False

    mid = len(data) // 2

    mid_value = data[mid]
    if target == mid_value:
        return True
    if target > mid_value:
        return binary_search(data[mid + 1:], target=target)
    return binary_search(data[:mid], target=target)


import bisect


if __name__ == '__main__':
    # binary search
    print(binary_search([1, 2, 3, 4], 4))