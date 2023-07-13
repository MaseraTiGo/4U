# -*- coding: utf-8 -*-
# @File    : __init__.py
# @Project : algorithm
# @Time    : 2023/3/31 21:55
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


class Solution15:
    def threeSum(self, nums: List[int]) -> List[List[int]]:
        if len(nums) == 3:
            return [nums] if not sum(nums) else []
        ret = []
        nums = sorted(nums)

        if nums[0] > 0 or nums[-1] < 0:
            return ret

        if not nums[0] and not sum(nums[:3]):
            return [[0, 0, 0]]

        first, last = 0, len(nums) - 1

        while nums[first] < 0:
            need_abs_val = abs(nums[first] + nums[first + 1])
            while nums[last] > 0:
                if need_abs_val > nums[last]:
                    break
                if need_abs_val == nums[last]:
                    ret.append([nums[first], nums[first + 1], nums[last]])
                    break
                last -= 1
            first += 1

        return ret


Solution15().threeSum([-1, 0, 1, 2, -1, -4])
