# -*- coding: utf-8 -*-
# @File    : lock_sme
# @Project : x_web
# @Time    : 2023/1/12 10:37
# once, I want 2 leave my name 2 the history
# sadly, I find that my hair gets pale
"""                     
                                      /             
 __.  , , , _  _   __ ______  _    __/  __ ____  _, 
(_/|_(_(_/_</_/_)_(_)/ / / <_</_  (_/_ (_)/ / <_(_)_
                                                 /| 
                                                |/  
"""
import time
from threading import Thread

import redis
from redis.lock import Lock

REDIS_CONF = {
    'host': 'localhost',
    'port': '6379',
    'max_connections': 100,
}


class RedisBase(object):

    def __init__(self, db=0):
        pool = redis.ConnectionPool(host=REDIS_CONF['host'],
                                    port=REDIS_CONF['port'],
                                    max_connections=int(
                                        REDIS_CONF['max_connections']), db=db)
        self.helper = redis.Redis(connection_pool=pool)

    def set(self, name, value, ex=None, px=None, nx=False,
            xx=False):
        return self.helper.set(name, value, ex, px, nx, xx)

    def get(self, name, invert=True):
        result = self.helper.get(name)
        result = result if result is None else result.decode()
        if invert and result is not None and result.isdigit():
            result = int(result)
        return result


def set_fuck_value(red_h, value):
    print(f"dong --------> not get fucking lock: {value}")
    with Lock(red_h, 'fucked', timeout=1000000):
        print(f"dong --------> get fucking lock: {value}\n")
        red_h.set('fuck', value)
        time.sleep(5)


if __name__ == '__main__':
    redis_sys = RedisBase(db=0)
    t2 = Thread(target=set_fuck_value, args=(redis_sys.helper, 'banana'))
    t1 = Thread(target=set_fuck_value, args=(redis_sys.helper, 'apple'))

    t1.start()
    t2.start()
    t1.join()
    t2.join()
    print(f'dong ------------------> all done')
    print(f'dong ------------------> ret: {redis_sys.get("fuck")}')
