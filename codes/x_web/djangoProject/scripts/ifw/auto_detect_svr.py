# -*- coding: utf-8 -*-
# @File    : auto_detect_svr
# @Project : djangoProject
# @Time    : 2022/11/2 11:22
# once, I want 2 leave my name 2 the history
# sadly, I find that my hair gets pale
"""                     
                                      /             
 __.  , , , _  _   __ ______  _    __/  __ ____  _, 
(_/|_(_(_/_</_/_)_(_)/ / / <_</_  (_/_ (_)/ / <_(_)_
                                                 /| 
                                                |/  
"""
import argparse
import signal
import socket
import sys
import threading
import time
from collections import defaultdict

COUNTER = defaultdict(int)
BREAK = False


def server(ss_ip: str, s_port: int, s_dp_size: int):
    global COUNTER
    s_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_addr = (ss_ip, s_port)
    s_socket.bind(server_addr)

    print(f'start receiving msg...')
    while 1:
        _, client = s_socket.recvfrom(s_dp_size)
        if _.decode() == 'fucking over':
            break
        c_ip, _ = client
        COUNTER[c_ip] += 1


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='auto server')
    parser.add_argument('-s', type=str, help='server ip, default=127.0.0.1')
    parser.add_argument('-sp', type=int, help='server port, default=5200')
    parser.add_argument('-d', type=int, help='duration(minute)')
    parser.add_argument('-dp_size', type=int, help='byte/per')
    args_p = parser.parse_args()

    if not args_p.d:
        print('duration time must be set.')
        sys.exit()

    s_ip = args_p.s
    if not s_ip:
        print('bind ip is not given, use default: 127.0.0.1')
        s_ip = '127.0.0.1'

    dp_size = args_p.dp_size
    if not dp_size:
        print('datagram size is not given, use default: 1024')
        dp_size = 1024

    port = 5200 if not args_p.sp else args_p.sp

    t = threading.Thread(target=server, args=(s_ip, port, dp_size))
    t.setDaemon(True)
    t.start()
    print(f'server is starting...')

    # server(s_ip, port, dp_size)

    try:
        time.sleep(args_p.d * 60)
    except KeyboardInterrupt:
        pass
    print(f'receive msg over, total: {dict(COUNTER)}')
