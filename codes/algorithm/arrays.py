# -*- coding: utf-8 -*-

# ===================================
# file_name     : arrays.py
# python_version: python 3.7.4
# file_author   : Johnathan.Strong
# create_time   : 2021/3/22 8:12
# ide_name      : PyCharm
# project_name  : 4U
# ===================================


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


# ================================================= 1480. Running Sum of 1d Array ======================================

class Solution1365:
    def smallerNumbersThanCurrent(self, nums: list) -> list:

        origin = nums[:]
        nums = sorted(nums)
        ans = {}
        for index, item in enumerate(nums):
            if item not in ans:
                ans[item] = index
        return [ans.get(i) for i in origin]


print(Solution1365().smallerNumbersThanCurrent([8, 1, 2, 2, 3]))
# ================================================= 1480. Running Sum of 1d Array ======================================