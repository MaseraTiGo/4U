# -*- coding: utf-8 -*-

# ===================================
# file_name     : arrays.py
# python_version: python 3.7.4
# file_author   : Johnathan.Strong
# create_time   : 2021/3/22 8:12
# ide_name      : PyCharm
# project_name  : 4U
# ===================================

from typing import List, Optional


# ================================================= 1313. Decompress Run-Length Encoded List ===========================

class Solution1313:
    def decompressRLElist(self, nums: list) -> list:
        process = [nums[2 * i: 2 * (i + 1)] for i in range(len(nums) // 2)]
        print(f'dong --------------->{process}')
        temp = []
        for item in process:
            temp.extend([item[1]] * item[0])
        return temp


nums = [1, 2, 3, 4]


# print(Solution1313().decompressRLElist(nums))

# ================================================= 1313. Decompress Run-Length Encoded List ===========================


# ================================================= 1365. How Many Numbers Are Smaller Than the Current Number =========

class Solution1365:
    def smallerNumbersThanCurrent(self, nums: list) -> list:

        origin = nums[:]
        nums = sorted(nums)
        ans = {}
        for index, item in enumerate(nums):
            if item not in ans:
                ans[item] = index
        return [ans.get(i) for i in origin]

# print(Solution1365().smallerNumbersThanCurrent([8, 1, 2, 2, 3]))
# ================================================= 1365. How Many Numbers Are Smaller Than the Current Number =========


# ================================================= 1389. Create Target Array in the Given Order =======================

class Solution1389:
    def createTargetArray(self, nums: List[int], index: List[int]) -> List[int]:
        target = []
        for i, value in enumerate(nums):
            target.insert(index[i], value)
        return target


# nums = [1, 2, 3, 4, 0]
# index = [0, 1, 2, 3, 0]
# print(Solution1389().createTargetArray(nums, index))


# ================================================= 1389. Create Target Array in the Given Order =======================


# ================================================= 1480. Running Sum of 1d Array ======================================

class Solution1480:
    def runningSum(self, nums: list) -> list:
        if not nums:
            return [0]

        ans = []
        temp = 0

        while nums:
            temp += nums.pop(0)
            ans.append(temp)
        return ans


# print(Solution1480().runningSum([1, 2, 3, 4, 5]))
# ================================================= 1480. Running Sum of 1d Array ======================================


# ================================================= 1486. XOR Operation in an Array ====================================

class Solution1486:
    def xorOperation(self, n: int, start: int) -> int:
        if not n:
            return 0
        gen_list = [start + 2 * i for i in range(n)]

        ans = gen_list[0]
        for item in gen_list[1:]:
            ans = ans ^ item

        return ans
# ================================================= 1486. XOR Operation in an Array ====================================



