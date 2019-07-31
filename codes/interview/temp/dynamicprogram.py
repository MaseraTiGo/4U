# -*- coding: utf-8 -*-
# file_func  :
# file_author: 'Johnathan.Wick'
# file_date  : '6/22/2019 8:17 AM'


def gold_miner(n, w, p, g):
    result = []
    pre_result = []
    for i in range(1, w + 1):
        result.append(0)
        if i >= p[0]:
            pre_result.append(g[0])
        else:
            pre_result.append(0)
    print('===============>', pre_result)
    for i in range(n):
        for j in range(w):
            if j < p[i]:
                result[j] = pre_result[j]
            else:
                result[j] = max(pre_result[j], pre_result[j - p[i]] + g[i])
        print('result is ---------------->', result)
        pre_result = result
    return result


def gold_miner_self(mines, workers, p, g):
    result = [0] * workers
    # pre_result = []
    for m in range(mines):
        for w in range(workers):
            if w + 1 < p[m]:
                result[w] = result[w]
            else:
                result[w] = max(result[w], result[w - p[m]] + g[m])
        print('----------->result', result)
    print('final is ============>', result)
    return result


n = 5
w = 10
g = [400, 500, 200, 300, 350]
p = [5, 5, 3, 4, 3]
# gold_miner_self(n, w, p, g)

import copy


def good(n, w, g=[], p=[]):
    arr = [0] * w
    for i in range(w):
        if (i + 1) >= p[0]:
            arr[i] = g[0]
    res = copy.deepcopy(arr)
    print(res)
    for i in range(1, n):
        for j in range(w):
            if (j + 1) < p[i]:
                arr[j] = res[j]
            else:
                t = 0 if (j - p[i]) < 0 else j - p[i]
                arr[j] = max(res[j], res[t] + g[i])
        res = copy.deepcopy(arr)
        print(res)
    return res.pop()


if __name__ == '__main__':
    res = good(5, 10, [400, 500, 200, 300, 350], [5, 5, 3, 4, 3])
