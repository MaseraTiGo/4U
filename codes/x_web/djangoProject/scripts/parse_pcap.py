# -*- coding: utf-8 -*-
# @File    : parse_pcap
# @Project : djangoProject
# @Time    : 2022/10/31 17:21
# once, I want 2 leave my name 2 the history
# sadly, I find that my hair gets pale
"""                     
                                      /             
 __.  , , , _  _   __ ______  _    __/  __ ____  _, 
(_/|_(_(_/_</_/_)_(_)/ / / <_</_  (_/_ (_)/ / <_(_)_
                                                 /| 
                                                |/  
"""

import dpkt


def sort_packets(path: str = None) -> list:
    with open('jun.pcap' if not path else path, 'rb') as fuck:
        pcap = dpkt.pcap.Reader(fuck)
        for timestamp, buf in pcap:
            print(f'dong -------> time: {timestamp}')
    return []

sort_packets()
