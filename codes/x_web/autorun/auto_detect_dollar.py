# -*- coding: utf-8 -*-
# @File    : auto_detect_dollar
# @Project : MyCareer
# @Time    : 2023/9/11 14:30
# once, I want 2 leave my name 2 the history
# sadly, I find that my hair gets pale
"""                     
                                      /             
 __.  , , , _  _   __ ______  _    __/  __ ____  _, 
(_/|_(_(_/_</_/_)_(_)/ / / <_</_  (_/_ (_)/ / <_(_)_
                                                 /| 
                                                |/  
"""
import ctypes
import os
import threading
import time as t_time
from datetime import datetime, time

import requests
from bs4 import BeautifulSoup

from super_dong.settings import PRINT_PREFIX


headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "en-GB,en;q=0.9,zh-CN;q=0.8,zh;q=0.7",
    "Cache-Control": "no-cache",
    "Connection": "keep-alive",
    "Cookie": "ASP.NET_SessionId=dvoo5u1epchhievcvdqxedag",
    "Host": "fx.cmbchina.com",
    "Pragma": "no-cache",
    "Sec-Ch-Ua": '"Google Chrome";v="113", "Chromium";v="113", "Not-A.Brand";v="24"',
    "Sec-Ch-Ua-Mobile": "?0",
    "Sec-Ch-Ua-Platform": '"Windows"',
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "same-origin",
    "Sec-Fetch-User": "?1",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36",
}


def give_me_the_soup(soup):
    currencies = soup.find_all('tr')
    for currency in currencies:
        dollar = currency.find('td', class_="fontbold")
        if not dollar:
            continue
        if currency.find('td', class_="fontbold").get_text(
                strip=True) == "美元":
            values = currency.find_all('td', class_="numberright")
            return [v.get_text(strip=True) for i, v in enumerate(values) if
                    i in [0, 2]]


def get_dollar():
    url = 'https://fx.cmbchina.com/api/v1/fx/rate'

    try:
        proxy = {
            "http": "127.0.0.1:7890",
            "https": "127.0.0.1:7890",
        }
        rsp = requests.get(url, headers=headers, proxies=proxy)
        # rsp = requests.get(url, headers=headers)
    except Exception as e:
        print(f"{PRINT_PREFIX} exception: {e}")
        return 0, 0
    data = rsp.json()
    for ccy in data['body']:
        if ccy.get('ccyNbr') == "美元":
            print(f"{PRINT_PREFIX} sell out: {ccy['rthOfr']}")
            print(f"{PRINT_PREFIX} buy in: {ccy['rthBid']}")
            return ccy['rthOfr'], ccy['rthBid']
    return 0, 0


def local_process():
    with open("test.html", encoding='utf-8') as shit:
        soup = BeautifulSoup(shit.read(), 'html.parser')
        return give_me_the_soup(soup)


def pop_msg(msg, flag):
    MB_ICON_INFORMATION = 0x40

    # Display a message box with an information icon
    ctypes.windll.user32.MessageBoxW(
        0,
        f"{msg}",
        f"NEW {flag} RECORD",
        MB_ICON_INFORMATION
    )


# Close the message box after a specified delay
def close_message_box_after_delay():
    t_time.sleep(15)
    ctypes.windll.user32.PostQuitMessage(0)


DEBUG = False

def dollar_run():
    from super_dong.model_store.models.model_my_money import DollarRate
    from django.db.models import Max, Min
    # Get the maximum value of your_field
    max_value = DollarRate.objects.aggregate(max_value=Max('sell_out'))[
        'max_value']

    if not max_value:
        max_value = float("-inf")
    # Get the minimum value of your_field
    min_value = DollarRate.objects.aggregate(min_value=Min('sell_out'))[
        'min_value']
    if not min_value:
        min_value = float("inf")

    while 1:
        current_time = datetime.now().time()

        start_time = time(9, 0)
        end_time = time(18, 0)

        # 判断当前时间是否在指定范围内
        if not (start_time <= current_time <= end_time):
            print(f"{PRINT_PREFIX} not running time.")
            t_time.sleep(60)
            continue
        s, b = local_process() if DEBUG else get_dollar()
        if not s:
            t_time.sleep(30)
            continue
        s, b = float(s), float(b)
        if s > max_value:
            print(f"{PRINT_PREFIX} NEW HIGH RECORD: {s}")
            threading.Thread(target=pop_msg, args=(s, 'HIGH')).start()
            # Create another thread to close the message box after a delay
            threading.Thread(target=close_message_box_after_delay).start()
            max_value = s
        if s < min_value:
            print(f"{PRINT_PREFIX} NEW LOW RECORD: {s}")
            threading.Thread(target=pop_msg, args=(s, 'LOW')).start()
            threading.Thread(target=close_message_box_after_delay).start()
            min_value = s
        try:
            DollarRate.create(sell_out=s, buy_in=b)
        except Exception as e:
            print(f"{PRINT_PREFIX} create exception: {e}")
            setup()

        t_time.sleep(30)


if __name__ == '__main__':
    from django import setup
    from django.db.models import Max, Min

    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djangoProject.settings')
    setup()

    dollar_run()
