# -*- coding: utf-8 -*-
# file_func  :
# file_author: 'Johnathan.Wick'
# file_date  : '6/21/2019 8:27 AM'

# version 2018 B
from copy import deepcopy


# No.1


class JGGSolution(object):
    """
    The basic idea: Arrange nine numbers, and then judge if the conditions are met.
    Time complexity: O(n!)
    space complexity: O(n)
    """

    def __init__(self, src_data: list):
        self._flag = False
        self._t_sum = None
        self._x_indexes = self._y_indexes = range(0, 3)
        self._src_data = src_data

    def solution(self, data, temp=[]):
        """

        :param data: nine numbers that be input
        :param temp: Store selected numbers
        :return: if the conditions are met, yield list of temp, or yield None
        """
        x_data = deepcopy(data)
        for index, item in enumerate(data):
            temp.append(item)
            if len(temp) == 9:
                if sum(temp[:3]) != self._t_sum:
                    self._flag = True
                if sum(temp[3:6]) != self._t_sum:
                    self._flag = True
                if temp[0] + temp[3] + temp[6] != self._t_sum or temp[2] + temp[4] + temp[6] != self._t_sum:
                    self._flag = True
                if temp[1] + temp[4] + temp[7] != self._t_sum:
                    self._flag = True
                if temp[0] + temp[4] + temp[8] != self._t_sum:
                    self._flag = True
                if self._flag:
                    yield
                else:
                    yield temp
                self._flag = False
            yield from self.solution(data[0:index] + data[index + 1:], temp)
            temp.pop()
            data = x_data

    def data_check(self):
        """
        do some prior checks
        :return: return a generator that can generate the lists that meet the conditions
        """
        # Determine whether the input data is an integer
        temp = [i for i in self._src_data if not isinstance(i, int)]
        if temp:
            print('invalid data')
            return
        # Preliminary Judgment on Solution
        self._src_data.sort()
        three_sum = self._src_data[3:6]
        if sum(self._src_data) != 3 * sum(self._src_data[3:6]):
            print('no solution!')
            return
        self._t_sum = sum(three_sum)
        s = self.solution(self._src_data)
        return s


# s = JGGSolution(list(range(11, 20)))
# for s_item in s.data_check():
#     if s_item:
#         for i in range(3):
#             print(s_item[i * 3:(i + 1) * 3])
#         print('---------------------------')


# No.2

class SecondIsland(object):
    """
    the basic idea: Using breadth-first algorithm(BFS)
    Time complexity: O(n)
    space complexity: O(1)
    """
    _directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]

    def __init__(self, data):
        self._data = data
        self._x_index_range = len(self._data)
        self._y_index_range = len(self._data[0])
        self._used_positions = []

    def get_second_island(self):
        """

        :return: the size of the island.
                if there does not exist island return zero.
                if there is only one island, return it.
                if there are more than two islands, Arrangement it from large to small, then return the second one.
        """
        temp = set()
        for x in range(self._x_index_range):
            for y in range(self._y_index_range):
                if (not self._data[x][y]) and (x not in [0, 5]) and (y not in [0, 5]) and (
                        (x, y) not in self._used_positions):
                    res = self.broad_first_search(x, y)
                    if res:
                        temp.add(res)
        temp = sorted(temp, reverse=True)
        if not temp:
            return 0
        temp = temp[0] if len(temp) == 1 else temp[1]
        return temp

    def broad_first_search(self, x, y):
        size = 1
        flag = False
        position = [(x, y)]
        self._used_positions = [(x, y)]
        while position:
            x, y = position.pop(0)
            for item in self._directions:
                new_x, new_y = x + item[0], y + item[1]
                if new_x < 0 or new_x >= self._x_index_range or new_y < 0 or new_y >= self._y_index_range:
                    continue
                if not self._data[new_x][new_y]:
                    if new_y in [0, 5] or new_x in [0, 5]:
                        size = 0
                        flag = True
                        break
                    if (new_x, new_y) not in self._used_positions:
                        size += 1
                        self._used_positions.append((new_x, new_y))
                        position.append((new_x, new_y))
                else:
                    continue
            if flag:
                break
        return size


src_data_2 = [[1, 1, 1, 1, 1, 1],
              [1, 1, 0, 0, 0, 1],
              [1, 0, 0, 0, 1, 0],
              [1, 1, 0, 1, 1, 1],
              [0, 1, 0, 1, 0, 0],
              [1, 1, 1, 1, 1, 1]]

# si = SecondIsland(src_data_2)
# second_island = si.get_second_island()
# print('second_island size is------------>:', second_island)

# No.3
import random


def generate_stock_price(days=5):
    res = random.choices(range(1, 10), k=days)
    return res


class StockSolution(object):
    @staticmethod
    def best_profit(prices):
        dp_1_0 = dp_2_0 = 0
        dp_1_1 = dp_2_1 = float('-inf')
        for price in prices:
            dp_1_1 = max(dp_1_1, -price)
            dp_1_0 = max(dp_1_0, dp_1_1 + price)
            dp_2_1 = max(dp_2_1, dp_1_0 - price)
            dp_2_0 = max(dp_2_0, dp_2_1 + price)
        return dp_2_0


# prices = generate_stock_price()
# print('prices============>', prices)
# # prices = [7, 4, 3, 1, 4]
# print(StockSolution.best_profit(prices))

# ---------------script for no.1-------------------------
# flag = False
#
#
# def generate(data, temp=[]):
#     global flag
#     x_data = deepcopy(data)
#     for index, item in enumerate(data):
#         temp.append(item)
#         if len(temp) == 9:
#             if sum(temp[:3]) != 15:
#                 flag = True
#             if sum(temp[3:6]) != 15:
#                 flag = True
#             if temp[0] + temp[3] + temp[6] != 15 or temp[2] + temp[4] + temp[6] != 15:
#                 flag = True
#             if temp[1] + temp[4] + temp[7] != 15:
#                 flag = True
#             if temp[0] + temp[4] + temp[8] != 15:
#                 flag = True
#             if flag:
#                 yield []
#             else:
#                 yield temp
#             flag = False
#         yield from generate(data[0:index] + data[index + 1:], temp)
#         temp.pop()
#         data = x_data
#
#
# src_data = [i for i in range(1, 10)]
# g = generate(src_data)
# for g_i in g:
#     if g_i:
#         print(g_i)
# ---------------script for no.1-------------------------

# ---------------script for no.2-------------------------

# src_data_2 = [[1, 1, 1, 1, 1, 1],
#               [1, 1, 0, 0, 0, 1],
#               [1, 0, 0, 0, 1, 0],
#               [1, 1, 0, 1, 1, 1],
#               [0, 1, 0, 1, 0, 0],
#               [1, 1, 1, 1, 1, 1]]
#
# x_indexes = len(src_data_2)
# y_indexes = len(src_data_2[0])
#
#
# def get_island(data):
#     temp = set()
#     for x in range(x_indexes):
#         for y in range(y_indexes):
#             if not data[x][y] and x not in [0, 5] and y not in [0, 5]:
#                 res = deep_search(x, y, data)
#                 if res:
#                     temp.add(res)
#     return temp
#
#
# DIRESCTION = [(-1, 0), (0, 1), (1, 0), (0, -1)]
#
#
# # BFS
# def deep_search(x, y, data):
#     c = 1
#     flag = False
#     position = [(x, y)]
#     used_position = [(x, y)]
#     temp = [(x, y)]
#     while position:
#         x, y = position.pop(0)
#         # used_position.append((x, y))
#         for item in DIRESCTION:
#             new_x, new_y = x + item[0], y + item[1]
#             if new_x < 0 or new_x >= x_indexes or new_y < 0 or new_y >= y_indexes:
#                 continue
#             if not data[new_x][new_y]:
#                 if new_y in [0, 5] or new_x in [0, 5]:
#                     c = 0
#                     flag = True
#                     break
#                 if (new_x, new_y) not in used_position:
#                     c += 1
#                     used_position.append((new_x, new_y))
#                     temp.append((new_x, new_y))
#                     position.append((new_x, new_y))
#             else:
#                 continue
#         if flag:
#             break
#     return c


# result = get_island(src_data_2)
# print(result)
# ---------------script for no.2-------------------------

# ---------------script for no.3-------------------------


# ---------------script for no.3-------------------------
