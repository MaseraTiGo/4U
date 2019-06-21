# -*- coding: utf-8 -*-
# file_func  : interview
# file_author: 'djd'
# file_date  : '6/21/2019 2:23 PM'

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


# No.3

class StockMaxProfit(object):
    """
    the basic idea: use dynamic programing algorithm
    not solved.

    """

    @staticmethod
    def max_profit(prices):
        pass
