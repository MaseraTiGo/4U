# -*- coding: utf-8 -*-
# file_func  :
# file_author: 'Johnathan.Wick'
# file_date  : '6/23/2019 7:58 AM'

import random
import copy


def get_integer(src_data: list, target: int):
    pre_result = [True]
    for i in range(1, target + 1):
        if i == src_data[0]:
            pre_result.append(True)
        else:
            pre_result.append(False)
    result = copy.deepcopy(pre_result)
    for item in src_data[1:]:
        for i in range(target + 1):
            if item > i + 1:
                pre_result[i] = result[i]
            else:
                pre_result[i] = result[i] or result[i - item]

        result = copy.deepcopy(pre_result)
        # print('-------------->result', result)
    return result[-1]


def get_integer_new(src_data: list, target: int):
    pre_result = [True]
    for i in range(1, target + 1):
        if i == src_data[0]:
            pre_result.append(True)
        else:
            pre_result.append(False)
    # result = copy.deepcopy(pre_result)
    result = pre_result
    for item in src_data[1:]:
        for i in range(target + 1):
            if item > i + 1:
                pre_result[i] = result[i]
            else:
                pre_result[i] = result[i] or result[i - item]

        result = copy.deepcopy(pre_result)
        # result = pre_result
        # print('-------------->result', result)
    return result[-1]


def generate_nine_nums(start=0, end=100, nums=9):
    return random.choices(range(start, end), k=nums)


# res = generate_nine_nums(end=10)
res = [3, 34, 4, 12, 5, 2]
print('res--------------->', res, sum(res))
print(get_integer_new(res, 9))
print(get_integer_new(res, 10))
print(get_integer_new(res, 11))
print(get_integer_new(res, 12))
print(get_integer_new(res, 13))
