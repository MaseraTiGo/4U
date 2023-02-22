# -*- coding: utf-8 -*-
# file_func  :
# file_author: 'Johnathan.Wick'
# file_date  : '5/11/2019 11:59 AM'
from collections import defaultdict


def optimal_solution(param: list):
    ret = defaultdict(int)

    sample_num, volunteer_num = param[0]
    efficiency = param[-1]
    base = {0: 0.2, 1: 0.1, 2: 0.1, 3: 0}

    for _ in range(volunteer_num):
        cur_delta_list = []
        for i in range(sample_num):
            cur_delta_list.append(efficiency[i] * base[ret[i]])
        cur_max_delta = max(cur_delta_list)
        if not cur_max_delta:
            break
        index = cur_delta_list.index(cur_max_delta)
        ret[index] += 1

    print(ret)


optimal_solution([[3, 12], [60, 70, 130]])
