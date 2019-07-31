# -*- coding: utf-8 -*-
# file_func  :
# file_author: 'Johnathan.Wick'
# file_date  : '6/25/2019 8:48 AM'
import random
from math import floor, ceil


def generate_nine_nums(start=0, end=100, nums=9):
    return random.choices(range(start, end), k=nums)


# ------------------------------------direct sort------------------------------

def direct_sort(src_data: list) -> list:
    _len = len(src_data)
    for i in range(1, _len):
        for j in range(i):
            if src_data[i] < src_data[j]:
                src_data.insert(j, src_data[i])
                src_data.pop(i + 1)
    return src_data


# direct_src_data = generate_nine_nums()
# print(direct_src_data)
# print(direct_sort(direct_src_data))


# ------------------------------------direct sort------------------------------

# ------------------------------------shell sort------------------------------
def shell_sort(src_data: list) -> list:
    _len = len(shell_src_data)
    half = _len % 2
    incr = _len / 2 if not half else (_len + 1) / 2
    step = int(incr)
    while step > 0:
        for i in range(step, _len):  # 在索引为step到len（L）上，比较L[i]和L[i-step]的大小
            print(step, src_data[i- step], src_data[i])
            while i >= step and src_data[i] < src_data[i - step]:  # 这里可以调整step从小到大或者从大到小排列
                src_data[i], src_data[i - step] = src_data[i - step], src_data[i]
                i -= step
        step /= 2
        step = int(step)
        print(src_data)
    return src_data


shell_src_data = generate_nine_nums(nums=10)
shell_src_data = [49, 38, 65, 97, 76, 13, 27, 49, 55, 4]
print('shell src data is===>', shell_src_data)
print(shell_sort(shell_src_data))
# ------------------------------------shell sort------------------------------
