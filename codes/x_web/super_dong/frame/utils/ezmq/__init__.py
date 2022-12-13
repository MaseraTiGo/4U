# -*- coding: utf-8 -*-
# @File    : __init__.py
# @Project : djangoProject
# @Time    : 2022/12/13 9:38
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
from threading import Thread

import zmq

from frame import DEFAULT_PREFIX

__all__ = ["ironman", 'ZmqServer']


class ZMQTaskManager(object):
    TASK_MAPPING = {
    }

    @classmethod
    def add(cls, key, func):
        cls.TASK_MAPPING[key] = func

    @classmethod
    def dispatch(cls, msg):
        msg = msg if msg else {}
        key = msg.get("key")
        if key not in cls.TASK_MAPPING:
            return
        kwargs = {}

        t = Thread(target=cls.TASK_MAPPING[key], args=(msg,), kwargs=kwargs)
        t.start()


def get_my_captain(host, port, timeout):
    context = zmq.Context()
    socket = context.socket(zmq.SUB)
    socket.setsockopt_string(zmq.SUBSCRIBE, '')
    if timeout:
        socket.setsockopt_string(zmq.RCVTIMEO, timeout)

    socket.connect("tcp://" + host + ":" + port)
    return socket


class ZmqServer(object):

    def __init__(self, address):
        context = zmq.Context()
        self.socket = context.socket(zmq.PUB)
        self.socket.bind(address)
        time.sleep(0.5)

    def loki_s_magic(self, msg, json_dumps=True):
        if json_dumps:
            msg = json.dumps(msg)
        self.socket.send_string(msg)


def ironman(host="127.0.0.1", port="5800", timeout=None):
    """
    接收底层的消息
    """
    print(
        f"{DEFAULT_PREFIX} zmq subscriber starts at port: {port}, ip: {host}"
    )
    captain_china = get_my_captain(host, port, timeout)
    while 1:
        try:
            msg = captain_china.recv_json(flags=zmq.NOBLOCK)
            if msg:
                print(f"{DEFAULT_PREFIX} zmq get msg: {msg}")
                ZMQTaskManager.dispatch(msg)
        except Exception as e:
            print(f"{DEFAULT_PREFIX} zmq get error: {e}")
        finally:
            time.sleep(0.5)


if __name__ == '__main__':
    ironman()
