# -*- coding: utf-8 -*-
# @File    : req
# @Project : x_web
# @Time    : 2023/1/13 16:02
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
import time

import requests

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36',
    'Cookie': 'OUTFOX_SEARCH_USER_ID_NCOO=647546686.8124081; OUTFOX_SEARCH_USER_ID="2010873550@10.110.96.158"; _ga=GA1.2.1200551767.1646874630; ACCSESSIONID=B3058A870C43CB6A0B930EE1E71B5ABC; __yadk_uid=KJr3rB5TlXG7jqgmFcglnheuB4GADliF; rollNum=true; DICT_FORCE=true; DICT_SESS=v2|ARUnmnQsZRUGO4YMRMUGRlMn4wBkfpF0QLhHqLhfpK0e4hfQ4RHJ40k5h4PSOLgF0eL0fTFhfl50QunLY5h4pL0wS64pFnfquR; DICT_LOGIN=1||1673580087057; advertiseCookie=advertiseValue; ___rl__test__cookies=1673591383783'

}

fail_repo = []


def _process_ret(ret):
    ret = json.loads(ret)
    if ret['code'] or ret['msg'] != 'SUCCESS':
        return False
    return True


def cancel_collect(word):
    url = f'https://dict.youdao.com/wordbook/webapi/v2/ajax/del?word={word}'

    ret = requests.get(url, headers=headers).content.decode()
    print(json.loads(ret))


def add_collect(word):
    url = f'https://dict.youdao.com/wordbook/webapi/v2/ajax/add?word={word}&lan=en'
    ret = requests.get(url, headers=headers).content.decode()
    print(f"dong --------->ret: {ret}")
    if not _process_ret(ret):
        print(f"dong -----------> fail word: {word}")
        fail_repo.append(word + '\n')


def write_2_txt(path):
    with open(path, 'w') as shit:
        shit.writelines(fail_repo)


if __name__ == '__main__':
    s = time.time()
    with open('TOEFL.txt') as shit:
        for m_line in shit.readlines():
            w = m_line.strip('\n')
            print(f"dong -----------> current word: {w}")
            add_collect(w)
    write_2_txt('req_fail.txt')
    print(f"dong ---------> cost: {time.time() - s}")
