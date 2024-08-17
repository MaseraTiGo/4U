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
import ipaddress
import time
from enum import Enum
from functools import wraps
from pprint import pprint

import requests

from super_dong.settings import PRINT_PREFIX as prefix


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


def auto_quick_create(interval=60, timing=9, end_date=None):
    created = {}

    while 1:
        date_time = datetime.datetime.now()
        date = date_time.date()

        if end_date:
            if str(date) == end_date:
                break

        cur_hour = date_time.hour
        if cur_hour in [timing, timing+3] and str(date) not in created:
            print(f"{prefix} quick create at: {str(date_time)}")
            Request.post(MyShitUrl.QUICK_CREATE.value, {"data": {"yesterday_only": False}})
            created[str(date)] = 1

        time.sleep(interval)
        print(f"{prefix} do it {interval} secs later......")


# from Crypto.Cipher import AES
#
#
# # data = b'secret data'
# #
# # key = get_random_bytes(16)
#
#
# def encrypt_aes(data, key):
#     data, key = data.encode(), key.encode()
#     cipher = AES.new(key, AES.MODE_EAX)
#     ciphertext, tag = cipher.encrypt_and_digest(data)
#     print(ciphertext, tag)
#     file_out = open("encrypted.bin", "wb")
#     [file_out.write(x) for x in (cipher.nonce, tag, ciphertext)]
#     file_out.close()
#
#
# def decrypt_are(key):
#     key = key.encode()
#     file_in = open("encrypted.bin", "rb")
#     nonce, tag, ciphertext = [file_in.read(x) for x in (16, 16, -1)]
#     file_in.close()
#
#     # let's assume that the key is somehow available again
#     cipher = AES.new(key, AES.MODE_EAX, nonce)
#     data = cipher.decrypt_and_verify(ciphertext, tag)
#     print(data.decode())
#
#
# # aes_key = "fuckyoustupidxxx"
# # # encrypt_aes("2023-04-17", aes_key)
# # decrypt_are(aes_key)
