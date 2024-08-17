# -*- coding: utf-8 -*-
# @File    : zmq_test
# @Project : 4U
# @Time    : 2024/8/16 11:26
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

import zmq


def zmq_send_2_5801(ip='192.178.562.32', port=5801, command=None, json_dumps=False):
    command = json.dumps(command) if json_dumps else command
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect('tcp://{ip}:{port}'.format(ip=ip, port=port))
    print(f"dong -------------------> send 2 5801: {command}")
    socket.send_json(command)
    msg = socket.recv_json()
    print(f"dong -------------------> receive from 5801: {msg}")
    return msg


if __name__ == '__main__':
    zmq_send_2_5801(command={'cmd': 'get_config'})
    from importlib import __import__
