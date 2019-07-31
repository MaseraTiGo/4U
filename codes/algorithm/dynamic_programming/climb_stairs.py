# -*- coding: utf-8 -*-
# file_func  :
# file_author: 'Johnathan.Wick'
# file_date  : '6/24/2019 5:45 PM'


def climb_stairs(k: int) -> int:
    solution = [0] * (k + 1)
    solution[0] = 0
    solution[1] = 1
    solution[2] = 2
    for i in range(3, k + 1):
        solution[i] = solution[i - 1] + solution[i - 2]
    return solution[-1]


# print(climb_stairs(10))

