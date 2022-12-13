# -*- coding: utf-8 -*-
# @File    : funcs
# @Project : hitler_adolf
# @Time    : 2022/6/10 9:31
"""                     
                                      /             
 __.  , , , _  _   __ ______  _    __/  __ ____  _, 
(_/|_(_(_/_</_/_)_(_)/ / / <_</_  (_/_ (_)/ / <_(_)_
                                                 /| 
                                                |/  
"""
import os
from datetime import date


def gen_today_log_path() -> str:
    today = str(date.today())
    return os.path.join('logs', f'{today}_cmd_record.log')
