# -*- coding: utf-8 -*-
# @File    : annuity
# @Project : x_web
# @Time    : 2023/6/25 19:11
# once, I want 2 leave my name 2 the history
# sadly, I find that my hair gets pale
"""                     
                                      /             
 __.  , , , _  _   __ ______  _    __/  __ ____  _, 
(_/|_(_(_/_</_/_)_(_)/ / / <_</_  (_/_ (_)/ / <_(_)_
                                                 /| 
                                                |/  
"""


def calculate_annuity_future_value(payment, interest_rate, periods):
    """
    计算普通年金的终值

    参数:
    payment (float): 每期支付金额
    interest_rate (float): 每个计息期的利率
    periods (int): 年金的总期数

    返回值:
    float: 年金的终值
    """
    future_value = payment * (
            (1 + interest_rate) ** periods - 1) / interest_rate
    return future_value


print("dong ----------------> final annuity: ",
      calculate_annuity_future_value(200, 0.08, 10))
