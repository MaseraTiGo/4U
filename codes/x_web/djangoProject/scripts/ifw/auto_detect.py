# -*- coding: utf-8 -*-
# @File    : auto_detect
# @Project : djangoProject
# @Time    : 2022/11/1 14:12
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
import ipaddress
import socket
import sys
import threading
import time
import timeit

COUNTER = 0
BREAK = False


class UdpSender(object):

    def __init__(self, server_ip: str, server_port: int = 5200,
                 client_ip: str = '127.0.0.1',
                 client_port: int = 5210,
                 duration: int = 3, rate: int = 1000,
                 send_msg: str = "just a test",
                 z: int = 1024,
                 x: int = 300
                 ):
        self._server = (server_ip, server_port)
        self._client = (client_ip, client_port)
        self._duration = duration
        self._rate = rate
        self.counter = 0
        self._msg = (send_msg * z).encode()
        self._x = x

    def send_upd_packets(self):
        global COUNTER
        c_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        c_socket.bind(self._client)

        while not BREAK:
            COUNTER += 1
            c_socket.sendto(self._msg, self._server)
            # time.sleep(1/self._rate)
            timeit.Timer('for i in range(33): oct(i)',
                         'gc.enable()').timeit(number=self._x)
        c_socket.sendto('fucking over'.encode(), self._server)


def run(sender_init_info: dict):
    udp_sender = UdpSender(**sender_init_info)
    t = threading.Thread(target=udp_sender.send_upd_packets)
    t.start()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='auto detect')
    parser.add_argument('-s', type=str, help='server ip')
    parser.add_argument('-sp', type=int, help='server port, default=5200')
    parser.add_argument('-c', type=str, help='client ip: default:127.0.0.1')
    parser.add_argument('-cp', type=int, help='server port, default=5210')
    parser.add_argument('-d', type=int, help='duration(minute)')
    parser.add_argument('-r', type=int, help='rate(per/second), default=1000(deprecated)')
    parser.add_argument('-m', type=str, help='send msg')
    parser.add_argument('-z', type=int, help='zoom out msg on "z" times')
    parser.add_argument('-x', type=int, help='xx using.')
    args = parser.parse_args()

    upd_sender_init_info = {}

    if not args.s:
        print(f"server ip must be given.")
        sys.exit()
    try:
        ipaddress.ip_address(args.s)
    except ValueError:
        print(f"{args.s} is not a valid ip")

    upd_sender_init_info['server_ip'] = args.s

    if args.sp:
        upd_sender_init_info['server_port'] = args.sp

    if args.c:
        try:
            ipaddress.ip_address(args.c)
        except ValueError:
            print(f"{args.c} is not a valid ip")
        upd_sender_init_info['client_ip'] = args.c

    if args.cp:
        upd_sender_init_info['client_port'] = args.cp

    if not args.d:
        print('duration time must be set.')
        sys.exit()
    upd_sender_init_info['duration'] = args.d

    if args.r:
        print(f'Attention: arg<rate> is deprecated! the value of it won\'t be used.')
        upd_sender_init_info['rate'] = args.r

    if args.m:
        upd_sender_init_info['send_msg'] = args.m

    if args.x is not None:
        if args.x <= 0:
            print('arg: x can not be less than 0.')
            sys.exit()
        upd_sender_init_info['x'] = args.x

    msg = 'default' if not args.m else args.m
    z = 1024 if not args.z else args.z
    upd_sender_init_info['z'] = z

    start_msg = f"start send msg: {msg} zoom out by {z} times(default) to {args.s} duration is {args.d} minutes"
    print(start_msg)

    run(upd_sender_init_info)

    try:
        time.sleep(args.d * 60)
    except KeyboardInterrupt:
        pass
    BREAK = True
    print(f'packets send 2: {args.s} over, total: {COUNTER}')
    sys.exit()
