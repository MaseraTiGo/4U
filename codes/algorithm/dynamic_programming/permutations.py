# -*- coding: utf-8 -*-
# file_func  :
# file_author: 'Johnathan.Wick'
# file_date  : '6/24/2019 6:09 PM'
import copy


class Solution:
    def permute(self, nums: list) -> list:
        # size = len(nums)
        # result = []
        #
        # def generate_permutations(nums, temp=[]):
        #     base_nums = copy.deepcopy(nums)
        #     for i, num in enumerate(nums):
        #         temp.append(num)
        #         if len(temp) == size:
        #             yield temp
        #         yield from generate_permutations(nums[:i] + nums[i + 1:], temp)
        #         nums = base_nums
        #         temp.pop()
        #
        # for i in generate_permutations(nums):
        #     result.append(i)
        # # return [copy.deepcopy(item) for item in generate_permutations(nums)]
        # return result
        result = []

        def traceback(nums, temp=[]):
            base_nums = copy.deepcopy(nums)
            for i, item in enumerate(nums):
                temp.append(item)
                nn = base_nums[:i] + base_nums[i + 1:]
                if not nn:
                    result.append(temp)
                traceback(nums, temp)
            nums = base_nums

        traceback(nums)
        print(result)


s = Solution()
res = s.permute([1, 2, 3])
print('result is res', res)
# res = s.permute([1])
# print('result is res', res)
# res = s.permute([])
# print('result is res', res)
