# -*- coding: utf-8 -*-
# file_func  :
# file_author: 'Johnathan.Wick'
# file_date  : '6/23/2019 2:41 PM'
"""
leetcode
"""

import timeit


# no.121
class Solution(object):
    @staticmethod
    def max_profit(prices: list) -> int:
        min_price = float('inf')
        max_profits = 0
        for p in prices:
            if p < min_price:
                min_price = p
            elif p - min_price > max_profits:
                max_profits = p - min_price
        return max_profits


src_data_1 = [7, 1, 5, 3, 6, 4]
src_data_2 = [7, 6, 4, 3, 1]


# s = Solution.max_profit(src_data_1)
# print('max_profit is:------------>', s)
# s = Solution.max_profit(src_data_2)
# print('max_profit is:------------>', s)


class Solution2:
    def maxProfit(self, prices: list) -> int:
        dp = [[0] * 3 for _ in range(len(prices))]
        dp[0][0] = 0
        dp[0][1] = -prices[0]
        dp[0][2] = 0
        for i in range(1, len(prices)):
            dp[i][0] = max(dp[i - 1][0], prices[i] + dp[i - 1][1], dp[i - 1][2])
            dp[i][1] = max(dp[i - 1][1], dp[i - 1][2] - prices[i])
            dp[i][2] = dp[i - 1][0]
        print('dp---------->', dp)
        return dp[-1][0]


# s = Solution2()
# s2_data_1 = [1, 2, 3, 0, 2]
# # s2_data_2 = [1, 2, 3, 0, 2]
# res = s.maxProfit(s2_data_1)
# print('res --------------->', res)


# res = s.maxProfit(s2_data_2)
# print('res --------------->', res)


class Solution3:
    def maxProfit(self, k: int, prices: list) -> int:
        if k == 0 or len(prices) < 2:
            return 0
        if k > len(prices) // 2:
            max_profit = 0
            for i in range(1, len(prices)):
                if prices[i] > prices[i - 1]:
                    max_profit += prices[i] - prices[i - 1]
            return max_profit
        else:
            buy = [float('-inf') for _ in range(k)]
            sell = [float('-inf') for _ in range(k)]
            for price in prices:
                buy[0] = max(buy[0], -price)
                sell[0] = max(sell[0], buy[0] + price)
                for i in range(1, k):
                    buy[i] = max(buy[i], sell[i - 1] - price)
                    sell[i] = max(sell[i], buy[i] + price)
            return sell[-1]


class Solution33:
    def maxProfit(self, k: int, prices: list) -> int:
        if len(prices) <= 1 or not k:
            return 0
        max_profit = 0
        if k > len(prices) / 2:
            for i in range(1, len(prices)):
                if prices[i] > prices[i-1]:
                    max_profit += prices[i] - prices[i-1]
        buy = [float('-inf')] * k
        # sell = [float('-inf')] * k
        sell = [0] * k
        for p in prices:
            buy[0] = max(buy[0], -p)
            sell[0] = max(sell[0], buy[0] + p)
            for i in range(1, k):
                buy[i] = max(buy[i], sell[i-1] - p)
                sell[i] = max(sell[i], buy[i] + p)
        return sell[-1]


s = Solution33()
s3_data_1 = [3, 2, 6, 5, 0, 3]
s3_data_2 = [2, 4, 1]
s3_data_3 = [1, 2, 4, 2, 5, 7, 2, 4, 9, 0]
s3_data_4 = [1, 2]
s3_data_5 = [3, 3, 5, 0, 0, 3, 1, 4]
k = 2
k2 = 4
k3 = 1
# res = s.maxProfit(k, s3_data_1)
# print('res --------------->', res)
# res = s.maxProfit(k, s3_data_2)
# print('res --------------->', res)
# res = s.maxProfit(k2, s3_data_3)
# print('res --------------->', res)
# res = s.maxProfit(k3, s3_data_4)
# print('res --------------->', res)
res = s.maxProfit(k, s3_data_5)
print('res --------------->', res)
