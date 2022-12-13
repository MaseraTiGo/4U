# -*- coding: utf-8 -*-
# @File    : host
# @Project : hitler_adolf
# @Time    : 2022/6/8 14:48
"""                     
                                      /             
 __.  , , , _  _   __ ______  _    __/  __ ____  _, 
(_/|_(_(_/_</_/_)_(_)/ / / <_</_  (_/_ (_)/ / <_(_)_
                                                 /| 
                                                |/  
"""

import socket


def give_mi_host_name() -> str:
    return socket.gethostname()


host_name = give_mi_host_name()


def give_mi_host_ip() -> str:
    return socket.gethostbyname(socket.gethostname())


host_ip = give_mi_host_ip()
