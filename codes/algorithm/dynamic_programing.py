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
