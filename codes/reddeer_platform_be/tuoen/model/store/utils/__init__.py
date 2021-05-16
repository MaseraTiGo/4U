# -*- coding: UTF-8 -*-    
# Author: Dongjd
# FileName: __init__.py
# DateTime: 2020/12/7 15:39
# Project: operate_backend_be
# Do Not Touch Me!

import time


def generate_uuid(prefix='', limit_len=False):
    random_str = str(time.time_ns())
    if limit_len and limit_len <= len(random_str):
        return prefix + random_str[-limit_len:]
    return prefix + random_str
