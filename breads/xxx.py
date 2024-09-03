# -*- coding: utf-8 -*-
# @File    : xxx
# @Project : 4U
# @Time    : 2024/8/16 15:58
# once, I want 2 leave my name 2 the history
# sadly, I find that my hair gets pale
"""                     
                                      /             
 __.  , , , _  _   __ ______  _    __/  __ ____  _, 
(_/|_(_(_/_</_/_)_(_)/ / / <_</_  (_/_ (_)/ / <_(_)_
                                                 /| 
                                                |/  
"""
import ipaddress
import re


class BusinessError(Exception):
    def __init__(self, message, en=None):
        self.message = message
        self.en = en if en else message


def is_valid_mac(mac):
    # 使用正则表达式验证MAC地址的合法性
    return re.match(r'^([0-9A-Fa-f]{2}-){5}([0-9A-Fa-f]{2})$', mac) is not None


def parse_ip_range(ip_range):
    start_ip, end_ip = ip_range.split('-')
    start_ip = ipaddress.IPv4Address(start_ip)
    end_ip = ipaddress.IPv4Address(end_ip)

    return [str(ip) for ip in range(int(start_ip), int(end_ip) + 1)]


def process_addresses(big_str):
    ip_addresses = set()
    mac_addresses = set()

    for item in big_str.split(','):
        item = item.strip()
        if '.' in item:
            try:
                if '/' in item:
                    network = ipaddress.IPv4Network(item, strict=False)
                    ip_addresses.update([str(ip) for ip in network.hosts()])
                elif '-' in item:
                    ip_addresses.update(parse_ip_range(item))
                else:
                    if ipaddress.IPv4Address(item):
                        ip_addresses.add(item)
            except Exception as e:
                raise BusinessError(f'无效的IP地址: {item}',
                                    en=f'Invalid IP address: {item}')
        else:
            if is_valid_mac(item):
                mac_addresses.add(item)
            else:
                raise BusinessError(f'无效的MAC地址: {item}',
                                    en=f'Invalid MAC address: {item}')
    print(f"ip numbers: {len(ip_addresses)}")
    print(f"mac numbers: {len(mac_addresses)}")
    if len(ip_addresses) > 256:
        raise BusinessError(
            "IP地址数量不能超过256个",
            en="IP address count cannot exceed 256"
        )
    if len(mac_addresses) > 16:
        raise BusinessError(
            "MAC地址数量不能超过16个",
            en="MAC address count cannot exceed 16"
        )

    return ip_addresses, mac_addresses


if __name__ == '__main__':
    # 示例输入
    input_str = "192.168.0.1,192.168.1.0-192.168.1.25,192.168.2.0/24,ac-ac-ac-ac-ac-ac,ab-cd-ef-12-34-56,09-07"

    # 处理输入
    ip_addresses, mac_addresses = process_addresses(input_str)

    # 输出结果
    print(f"Valid IP addresses ({len(ip_addresses)}): {sorted(ip_addresses)}")
    print(
        f"Valid MAC addresses ({len(mac_addresses)}): {sorted(mac_addresses)}")
