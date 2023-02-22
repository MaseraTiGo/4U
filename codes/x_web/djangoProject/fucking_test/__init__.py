# -*- coding: utf-8 -*-
# @File    : __init__.py
# @Project : djangoProject
# @Time    : 2022/10/26 16:50
# once, I want 2 leave my name 2 the history
# sadly, I find that my hair gets pale
"""                     
                                      /             
 __.  , , , _  _   __ ______  _    __/  __ ____  _, 
(_/|_(_(_/_</_/_)_(_)/ / / <_</_  (_/_ (_)/ / <_(_)_
                                                 /| 
                                                |/  
"""
import json


class Mgmt(object):

    def __init__(self, flag):
        self.flag = flag

    def __enter__(self):
        if self.flag == 'fuck':
            raise ValueError
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        print(exc_type)
        print(exc_val)
        print(exc_tb)

a = [
        {
            "group_id": 1,
            "group": [
                {
                    "sche_type": "period_day",
                    "sche_time": "Monday,Tuesday,Wednesday,Thursday,Friday,Saturday",
                    "start_time": "14:18",
                    "end_time": "14:19"
                }
            ]
        },
        {
            "group_id": 2,
            "group": [
                {
                    "sche_type": "period_date",
                    "sche_time": "2021-10-08,2021-10-10",
                    "start_time": "14:22",
                    "end_time": "14:23"
                }
            ]
        }
    ]


print(len(json.dumps(a, separators=(',', ':'))))