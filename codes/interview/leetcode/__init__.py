# -*- coding: utf-8 -*-
# file_func  :
# file_author: 'Johnathan.Wick'
# file_date  : '6/25/2019 11:32 AM'

# no.26
class Solution:
    def removeDuplicates(self, nums: list) -> int:
        # j = 0
        # for i in range(1, len(nums)):
        #     if nums[j] == nums[i]:
        #         continue
        #     else:
        #         j += 1
        #         nums[j] = nums[i]
        # return len(nums)
        for i in range(len(nums) - 1, 0, -1):
            if nums[i] == nums[i - 1]:
                nums.pop(i)
        print(nums)
        return len(nums)


# Solution().removeDuplicates([1, 1, 2, 2, 2, 3, 4, 5, 6, 6])


class Solution2:
    def findMedianSortedArrays(self, nums1: list, nums2: list) -> float:
        new_list = nums1 + nums2
        _len = len(new_list)
        new_list = sorted(new_list)
        if _len % 2 != 0:
            from math import floor
            return float(new_list[floor(_len / 2)])
        else:
            return new_list[int(_len / 2)] + new_list[int(_len / 2) - 1] / 2


res = Solution2().findMedianSortedArrays([1, 3], [2])
print(res)
