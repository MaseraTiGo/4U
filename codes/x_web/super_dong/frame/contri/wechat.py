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
import json
import time
from enum import Enum

import requests

from funds.funds import Founds
from super_dong.settings import PRINT_PREFIX as prefix


class WeChatReceiver(object):
    ...


class WeChatSender(object):
    ...


class WeChatWatchDog(object):
    ...


class MyShitUrl(str, Enum):
    QUICK_CREATE = 'http://192.168.203.51:8888/apis/admin/money/quickcreate'


class Request(object):

    @classmethod
    def post(cls, url, data):
        requests.post(url, json=data)


def auto_quick_create(interval=60, timing=9, end_date=None):
    created = {}
    while 1:
        date_time = datetime.datetime.now()
        date = date_time.date()

        if end_date:
            if str(date) == end_date:
                break

        cur_hour = date_time.hour
        if cur_hour in [timing, timing + 5] and str(date) not in created:
            print(f"{prefix} quick create at: {str(date_time)}")
            Request.post(MyShitUrl.QUICK_CREATE.value,
                         {"data": {"yesterday_only": False}})
            created[str(date)] = 1

        time.sleep(interval)
        print(f"{prefix} do it {interval} secs later......")
    cal_new_amount_and_update()


def cal_new_amount_and_update():
    today = datetime.datetime.today()
    from super_dong.models import MyShit
    my_shits = MyShit.objects.filter(create_time__date=today)
    founds_code_mapping = {
        json.loads(item.remark)['fcode']: item
        for item in my_shits if json.loads(item.remark)
    }
    for fcode, shit in founds_code_mapping.items():
        if shit.ex_info.get('regular_invest'):
            ... # todo
        else:
            process_normal_founds(fcode, shit)


def process_normal_founds(fcode, shit):
    newest_networth = Founds.get_funds(fcode)
    if not newest_networth:
        return
    shit.amount = float('%.2f' % (shit.share * newest_networth))
    shit.save()
