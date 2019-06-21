# -*- coding: utf-8 -*-
# file_func  :
# file_author: 'Johnathan.Wick'
# file_date  : '6/21/2019 4:41 PM'
import random
import unittest

from zingfront import JGGSolution, SecondIsland, StockMaxProfit


# generate random integer nums
def generate_nine_nums(start=0, end=100, nums=9):
    return random.choices(range(start, end), k=nums)


class TestJGGSolution(unittest.TestCase):

    def test_jgg(self):
        for _ in range(5):
            src_nums = generate_nine_nums()
            print('------------>src_nums:', src_nums)
            s = JGGSolution(src_nums)
            g = s.data_check()
            if g:
                for g_item in g:
                    if g_item:
                        for i in range(3):
                            print(g_item[i * 3:(i + 1) * 3])
                        print('---------------------------')

    def test_jgg2(self):
        s = JGGSolution(list(range(1, 10)))
        g = s.data_check()
        for g_item in g:
            if g_item:
                for i in range(3):
                    print(g_item[i * 3:(i + 1) * 3])
                print('---------------------------')


class TestSecondIsland(unittest.TestCase):
    _src_data_1 = [[1, 1, 1, 1, 1, 1],
                   [1, 1, 0, 0, 0, 1],
                   [1, 0, 0, 0, 1, 0],
                   [1, 1, 0, 1, 1, 1],
                   [0, 1, 0, 1, 0, 0],
                   [1, 1, 1, 1, 1, 1]]

    _src_data_2 = [[1, 1, 1, 1, 1, 1],
                   [1, 1, 0, 0, 0, 1],
                   [1, 0, 0, 0, 1, 0],
                   [1, 1, 0, 1, 1, 1],
                   [0, 1, 0, 1, 0, 1],
                   [1, 1, 1, 1, 1, 1]]

    _src_data_3 = [[1, 1, 1, 1, 1, 1],
                   [1, 1, 0, 0, 0, 1],
                   [1, 0, 0, 0, 1, 0],
                   [1, 1, 0, 1, 0, 1],
                   [0, 1, 0, 1, 0, 1],
                   [1, 1, 1, 1, 1, 1]]

    def test_src1(self):
        si = SecondIsland(TestSecondIsland._src_data_1)
        second = si.get_second_island()
        self.assertEqual(second, 8)
        print('test src_data_1 success')

    def test_src2(self):
        si = SecondIsland(TestSecondIsland._src_data_2)
        second = si.get_second_island()
        self.assertEqual(second, 1)
        print('test src_data_2 success')

    def test_src3(self):
        si = SecondIsland(TestSecondIsland._src_data_3)
        second = si.get_second_island()
        self.assertEqual(second, 2)
        print('test src_data_3 success')


class TestMaxProfit(unittest.TestCase):
    _src_data_1 = [1, 2, 3, 4, 5]

    def test_profit_1(self):
        # profit = StockMaxProfit.max_profit(TestMaxProfit._src_data_1)
        # print('-------------->max_profit', profit)
        pass


if __name__ == '__main__':
    unittest.main()
