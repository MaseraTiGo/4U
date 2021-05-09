# -*- coding: utf-8 -*-
# @File    : dynamic_programing.py
# @Project : 4U
# @Time    : 2021/4/20 9:35

"""                     
                                      /             
 __.  , , , _  _   __ ______  _    __/  __ ____  _, 
(_/|_(_(_/_</_/_)_(_)/ / / <_</_  (_/_ (_)/ / <_(_)_
                                                 /| 
                                                |/
"""

from codes.algorithm import print_


def get_my_dp(m, n):
    return [[None for _ in range(n)] for _ in range(m)]


# ================================================= get my fucking target===============================================

class SolutionFucking001:
    def solve(self, n):
        dp = [None for _ in range(n + 1)]
        dp[0] = 0
        dp[1] = 1
        dp[2] = 1
        dp[3] = 2
        dp[4] = 3
        dp[5] = 5

        if dp[n] is not None:
            return dp[n]

        for i in range(6, n + 1):
            dp[i] = dp[i - 1] + dp[i - 3] + dp[i - 5]
        return dp[n]


print(f'dong --------------->{SolutionFucking001().solve(5)}')


# ================================================= get my fucking target===============================================


# ================================================= 53. Maximum Subarray ===============================================

# Runtime: 64 ms, faster than 72.43% of Python3 online submissions for Maximum Subarray.
# Memory Usage: 14.9 MB, less than 79.49% of Python3 online submissions for Maximum Subarray.
class Solution53:
    def maxSubArray(self, nums: List[int]) -> int:
        maximum = nums[0]
        cur_max = nums[0]
        if len(nums) == 1:
            return maximum
        for i in range(1, len(nums)):
            cur_max = max(nums[i], nums[i] + cur_max)
            maximum = max(maximum, cur_max)
        return maximum


# print(Solution53().maxSubArray([-2, 1, -3, 4, -1, 2, 1, -5, 4]))


# ================================================= 53. Maximum Subarray ===============================================


# ================================================= 62. Unique Paths ===================================================

# Runtime: 28 ms, faster than 84.82% of Python3 online submissions for Unique Paths.
# Memory Usage: 14.7 MB, less than 7.18% of Python3 online submissions for Unique Paths.
class Solution62:

    def solve(self, m, n):
        dp = [[None for _ in range(n)] for _ in range(m)]
        for i in range(m):
            dp[i][0] = 1
        for i in range(n):
            dp[0][i] = 1

        def helper(m, n):
            if dp[m][n] is not None:
                return dp[m][n]
            else:
                dp[m][n] = helper(m - 1, n) + helper(m, n - 1)
                return dp[m][n]

        ans = helper(m - 1, n - 1)
        return ans


# print(Solution62().solve(3, 3))
# ================================================= 62. Unique Paths ===================================================


# ================================================= 64. Minimum Path Sum ===============================================


# Runtime: 100 ms, faster than 52.92% of Python3 online submissions for Minimum Path Sum.
# Memory Usage: 16.2 MB, less than 15.21% of Python3 online submissions for Minimum Path Sum.
class Solution64:
    def solve(self, grid):
        m = len(grid)
        n = len(grid[0])
        dp = [[None for _ in range(n)] for _ in range(m)]
        dp[0][0] = grid[0][0]
        for i in range(1, m):
            dp[i][0] = dp[i - 1][0] + grid[i][0]
        for j in range(1, n):
            dp[0][j] = dp[0][j - 1] + grid[0][j]

        def helper(m, n):
            if dp[m][n] is not None:
                return dp[m][n]
            dp[m][n] = min(helper(m - 1, n), helper(m, n - 1)) + grid[m][n]
            return dp[m][n]

        ans = helper(m - 1, n - 1)
        return ans


# print(Solution64().solve([[1, 2, 3], [4, 5, 6]]))
# ================================================= 64. Minimum Path Sum ===============================================


# ================================================= 70. Climbing Stairs ================================================

# Runtime: 24 ms, faster than 92.73% of Python3 online submissions for Climbing Stairs.
# Memory Usage: 14.2 MB, less than 43.97% of Python3 online submissions for Climbing Stairs.
class Solution70:
    def __init__(self):
        self.caching = {1: 1, 2: 2}

    def climbStairs(self, n: int) -> int:
        if n in self.caching:
            return self.caching.get(n)
        res = self.climbStairs(n - 1) + self.climbStairs(n - 2)
        self.caching[n] = res
        return res


# print(Solution70().climbStairs(30))


# ================================================= 70. Climbing Stairs ================================================


# ================================================= 72. Edit Distance ==================================================

# Runtime: 160 ms, faster than 75.75% of Python3 online submissions for Edit Distance.
# Memory Usage: 17.8 MB, less than 43.70% of Python3 online submissions for Edit Distance.
class Solution72:
    def solve(self, word1, word2):
        len_1 = len(word1)
        len_2 = len(word2)
        dp = [[None for _ in range(len_2 + 1)] for _ in range(len_1 + 1)]
        dp[0][0] = 0
        for i in range(1, len_1 + 1):
            dp[i][0] = dp[i - 1][0] + 1
        for j in range(1, len_2 + 1):
            dp[0][j] = dp[0][j - 1] + 1
        for i in range(len_1):
            for j in range(len_2):
                if word1[i] == word2[j]:
                    dp[i + 1][j + 1] = dp[i][j]
                else:
                    dp[i + 1][j + 1] = min(dp[i][j + 1], dp[i][j], dp[i + 1][j]) + 1
        return dp[len_1][len_2]


# print(Solution72().solve("intention", "execution"))
# ================================================= 72. Edit Distance ==================================================


# ================================================= 121. Best Time to Buy and Sell Stock ===============================

# Runtime: 972 ms, faster than 74.01% of Python3 online submissions for Best Time to Buy and Sell Stock.
# Memory Usage: 25.1 MB, less than 52.84% of Python3 online submissions for Best Time to Buy and Sell Stock.
class Solution121:
    def maxProfit(self, prices: List[int]) -> int:
        buy = prices[0]
        maximum = 0

        for price in prices[1:]:
            if price < buy:
                buy = price
            maximum = max(maximum, price - buy)
        return maximum


# print(Solution121().maxProfit([7, 1, 5, 3, 6, 4]))


# ================================================= 121. Best Time to Buy and Sell Stock ===============================


# ================================================= 303. Range Sum Query - Immutable ===================================

# Runtime: 68 ms, faster than 97.89% of Python3 online submissions for Range Sum Query - Immutable.
# Memory Usage: 17.9 MB, less than 20.74% of Python3 online submissions for Range Sum Query - Immutable.
class Solution303:

    def __init__(self, nums: List[int]):
        self.nums = nums
        self.dp = [0 for _ in range(len(nums) + 1)]
        for i in range(1, len(nums) + 1):
            self.dp[i] = self.dp[i - 1] + self.nums[i - 1]

    def sumRange(self, left: int, right: int) -> int:
        return self.dp[right + 1] - self.dp[left]


# obj = Solution303([-2, 0, 3, -5, 2, -1])
# print(obj.sumRange(0, 5))


# Your NumArray object will be instantiated and called as such:
# obj = NumArray(nums)
# param_1 = obj.sumRange(left,right)
# ================================================= 303. Range Sum Query - Immutable ===================================


# ================================================= 338. Counting Bits =================================================

# Runtime: 216 ms, faster than 10.68% of Python3 online submissions for Counting Bits.
# Memory Usage: 20.8 MB, less than 74.21% of Python3 online submissions for Counting Bits.
class Solution338:
    def countBits(self, num: int) -> List[int]:
        from collections import Counter
        src = []

        def counter(n):
            return [Counter(bin(n)).get("1", 0)]

        for i in range(num + 1):
            src += counter(i)

        return src


# print(Solution338().countBits(5))


# ================================================= 338. Counting Bits =================================================


# ================================================= 392. Is Subsequence ================================================

# Runtime: 24 ms, faster than 95.66% of Python3 online submissions for Is Subsequence.
# Memory Usage: 14.2 MB, less than 73.55% of Python3 online submissions for Is Subsequence.
class Solution392:
    def isSubsequence(self, s: str, t: str) -> bool:
        if not t and s:
            return False
        if not s:
            return True
        start, end = 0, len(t)
        if s[0] not in t[start: end]:
            return False
        pre_bool = True
        for i in range(1, len(s)):
            try:
                start = t.index(s[i - 1])
            except ValueError as _:
                return False
            t = t[start + 1: end]
            pre_bool = pre_bool and s[i] in t
        return pre_bool

    def approach_two(self, s, t):
        i = 0
        j = 0
        while i < len(s) and j < len(t):
            if s[i] == t[j]:
                i = i + 1
            j = j + 1
        return i == len(s)


# print(Solution392().isSubsequence("aaaaaa", "bbaaaa"))


# ================================================= 392. Is Subsequence ================================================


# ================================================= 1025. Divisor Game =================================================

class Solution1025:
    def solve(self, n):
        if n < 2:
            return False


# ================================================= 1025. Divisor Game =================================================


# ================================================= 1043. Partition Array for Maximum Sum ==============================

class Solution1043:
    def maxSumAfterPartitioning(self, arr: List[int], k: int) -> int:
        if k == 1:
            return sum(arr)
        if k == len(arr):
            return k * max(arr)

        ...


# ================================================= 1043. Partition Array for Maximum Sum ==============================


# ================================================= 1130. Minimum Cost Tree From Leaf Values ===========================

class Solution1130:
    def mctFromLeafValues(self, arr: List[int]) -> int:
        return 0


# ================================================= 1130. Minimum Cost Tree From Leaf Values ===========================


# ================================================= 1641. Count Sorted Vowel Strings ===================================

class Solution1641:
    def __init__(self):
        self.dp = None

    def countVowelStrings(self, n: int) -> int:
        if n == 1:
            return 5
        res = self.countVowelStrings(n - 1) + (n - 1) * 10
        return res

# print(Solution1641().countVowelStrings(4))

# ================================================= 1641. Count Sorted Vowel Strings ===================================
