# -*- coding: utf-8 -*-
# @File    : test_redis
# @Project : hitler_adolf
# @Time    : 2022/6/9 11:49
"""                     
                                      /             
 __.  , , , _  _   __ ______  _    __/  __ ____  _, 
(_/|_(_(_/_</_/_)_(_)/ / / <_</_  (_/_ (_)/ / <_(_)_
                                                 /| 
                                                |/  
"""
import time

from utils.redis_op import redis_trans_broker


def get_res(key, time_out: int = None,
            interval: float = None,
            res_num: int = None) -> dict:
    loop = int(time_out / interval)

    keys = None

    while loop:
        try:
            keys = redis_trans_broker.keys(f'{key}-*')
            if len(keys) != res_num:
                continue

            res = redis_trans_broker.mget(keys, prefix=False, jsonify=True)
            return {
                "result": dict(zip(keys, res)),
                "code": 0
            }
        except Exception as e:
            print(f"dong ------------>e: {e}")
        finally:
            time.sleep(interval)
            loop -= 1
    return {
        "result": f"something goes wrong and timeout: {keys}",
        "code": 1
    }
