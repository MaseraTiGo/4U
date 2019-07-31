# -*- coding: utf-8 -*-
# file_func  :
# file_author: 'Johnathan.Wick'
# file_date  : '6/23/2019 9:54 AM'

from copy import deepcopy


def give_change(coins: list, target: int) -> int:
    pre_result = [0] * (target + 1)
    for i in range(1, target + 1):
        pre_result[i] = i
    for coin in coins:
        for i in range(1, target + 1):
            if coin > i:
                pre_result[i] = pre_result[i]
            else:
                pre_result[i] = min(pre_result[i], pre_result[i - coin] + 1)

    return pre_result


coins = [1, 2, 5, 10]
target = 33
least = give_change(coins, target)
print('at least, it needs :', least)
