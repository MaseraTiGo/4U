# -*- coding: utf-8 -*-
# @File    : wechat
# @Project : x_web
# @Time    : 2023/2/9 14:19
# once, I want 2 leave my name 2 the history
# sadly, I find that my hair gets pale
"""                     
                                      /             
 __.  , , , _  _   __ ______  _    __/  __ ____  _, 
(_/|_(_(_/_</_/_)_(_)/ / / <_</_  (_/_ (_)/ / <_(_)_
                                                 /| 
                                                |/  
"""

import datetime
import time
from enum import Enum

import requests

prefix = 'dong ------------->'


class WeChatReceiver(object):
    ...


class WeChatSender(object):
    ...


class WeChatWatchDog(object):
    ...


class MyShitUrl(str, Enum):
    QUICK_CREATE = 'http://192.168.203.51:8000/apis/admin/money/quickcreate'


class Request(object):

    @classmethod
    def post(cls, url, data):
        requests.post(url, json=data)


def auto_quick_create(interval=60, timing=10, end_date=None):
    created = {}

    while 1:
        date_time = datetime.datetime.now()
        date = date_time.date()

        if end_date:
            if str(date) == end_date:
                break

        cur_hour = date_time.hour
        if cur_hour == timing and str(date) not in created:
            print(f"{prefix} quick create at: {str(date_time)}")
            Request.post(MyShitUrl.QUICK_CREATE.value, {"data": {}})
            created[str(date)] = 1

        time.sleep(interval)
        print(f"{prefix} do it {interval} secs later......")


auto_quick_create()
