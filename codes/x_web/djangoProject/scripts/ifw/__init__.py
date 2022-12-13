# -*- coding: utf-8 -*-
# @File    : __init__.py
# @Project : djangoProject
# @Time    : 2022/11/1 14:12
# once, I want 2 leave my name 2 the history
# sadly, I find that my hair gets pale
"""                     
                                      /             
 __.  , , , _  _   __ ______  _    __/  __ ____  _, 
(_/|_(_(_/_</_/_)_(_)/ / / <_</_  (_/_ (_)/ / <_(_)_
                                                 /| 
                                                |/  
"""
from datetime import datetime, timedelta


def get_fucking_export_days(days: int = 13):
    today = datetime.today()
    day_str = []
    for _ in range(days):
        del_day = timedelta(days=_)
        day_str.append((today - del_day).strftime("%Y%m%d"))
    return day_str


print(get_fucking_export_days())
