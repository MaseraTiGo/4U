from typing import List, Optional
import random


def give_me_some_random_nums(num=7, start=0, end=99):
    result = [random.randint(start, end) for _ in range(num)]
    print(f'dong ------------------->random nums: {result}')
    return result


# ================================================= common funcs =======================================================


# selection sort
def selection_sort(src_list):
    minimum = float('inf')
    maximum = float('-inf')
    l_len = len(src_list) - 1
    for i in range(len(src_list)):
        e = l_len - i
        if i == e:
            break
        for item in src_list[i:e + 1]:
            minimum = min(minimum, item)
            maximum = max(maximum, item)
        j = src_list.index(minimum)
        m = src_list.index(maximum)
        src_list[i], src_list[j] = src_list[j], src_list[i]
        src_list[e], src_list[m] = src_list[m], src_list[e]
        minimum = float('inf')
        maximum = float('-inf')
    return src_list


# print(selection_sort([1, 4, 3, 5, 2, 7, 9, 6, 8]))


# insert sort
def insertion_sort(src_list):
    src_len = len(src_list)
    for i in range(src_len):
        current = src_list[i]
        animation_pos = i
        while animation_pos > 0 and src_list[animation_pos - 1] > current:
            src_list[animation_pos] = src_list[animation_pos - 1]
            animation_pos -= 1
        src_list[animation_pos] = current
    return src_list


# bubble sort
def bubble_sort(src_list):
    for i, item in enumerate(src_list):
        for j in range(i + 1, len(src_list)):
            if item > src_list[j]:
                src_list[i], src_list[j] = src_list[j], src_list[i]
    return src_list


# shell sort
def shell_sort(src_list):
    n = len(src_list)
    gap = int(n / 2)
    while gap > 0:
        for i in range(gap, n):
            temp = src_list[i]
            j = i - gap
            while j >= 0 and src_list[j] > temp:
                src_list[j + gap] = src_list[j]
                j = j - gap
            src_list[j + gap] = temp
        gap = int(gap / 2)
    return src_list


# merge sort
def merge_core(list_one, list_two=None):
    if not list_two:
        return list_one
    temp = []

    i = j = 0
    while 1:
        if i == len(list_one) or j == len(list_two):
            break
        if list_one[i] < list_two[j]:
            temp.append(list_one[i])
            i += 1
        elif list_one[i] == list_two[j]:
            temp.extend([list_one[i]] * 2)
            i += 1
            j += 1
        else:
            temp.append(list_two[j])
            j += 1
    temp.extend(list_one[i:])
    temp.extend(list_two[j:])
    return temp


# print(merge_core([1, 3, 5, 5, 7, 9], [0, 2, 4, 6, 6, 8]))

merge_ans = []


def merge_sort(src_list):
    if len(src_list) <= 1:
        return src_list
    mid = int(len(src_list) // 2)
    left = merge_sort(src_list[: mid])
    right = merge_sort(src_list[mid:])
    res = merge_core(left, right)
    return res


print(merge_sort(give_me_some_random_nums()))


# ================================================= common funcs =======================================================


# ================================================= 1528. Shuffle String ===============================================

class Solution1528:
    def restoreString(self, s: str, indices: List[int]) -> str:
        ans = [''] * len(s)
        for i in range(len(s)):
            ans[indices[i]] = s[i]
        return ''.join(ans)

# s_src = "codeleet"
# indices_src = [4, 5, 6, 7, 0, 2, 1, 3]
# print(Solution1528().restoreString(s_src, indices_src))
# ================================================= 1528. Shuffle String ===============================================
