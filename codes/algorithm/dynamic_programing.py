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
