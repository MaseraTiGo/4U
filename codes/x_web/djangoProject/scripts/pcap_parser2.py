# -*- coding: utf-8 -*-
# @File    : pcap_parser2
# @Project : djangoProject
# @Time    : 2022/10/31 17:32
# once, I want 2 leave my name 2 the history
# sadly, I find that my hair gets pale
"""                     
                                      /             
 __.  , , , _  _   __ ______  _    __/  __ ____  _, 
(_/|_(_(_/_</_/_)_(_)/ / / <_</_  (_/_ (_)/ / <_(_)_
                                                 /| 
                                                |/  
"""

from scapy.all import *


def writefile(filename, stringlist):
    f = open("dong.txt", "w")
    for i in stringlist:
        f.write(i + "\n")
    f.close()


def search(filename):
    filepath = filename
    stringlist = []
    pcaps = rdpcap(filepath)
    print(len(pcaps))
    for p in pcaps:
        print(p.__class__)
        print(p.payload.__class__)
        print(p.payload.payload.__class__)
        print(p.payload.payload.__class__)
        for f in p.fields_desc:
            fvalue = p.getfieldval(f.name)
            print(f'dong ------------>{f.name}: {fvalue}')
            # reprval = f.i2repr(p.payload, fvalue)  # 转换成十进制字符串
            # print(f.name)
            # if str(f.name) == "src":  # 指定特定的ip地址
            #     for f2 in p.payload.payload.payload.payload.fields_desc:  # payload向下解析一层
            #         # print f2.name
            #         if f2.name == "load" or f2.name == "data":
            #             fvalue = p.payload.getfieldval(f2.name)
            #             reprval = f2.i2repr(p.payload, fvalue)
            #             refind = re.compile(r'[A-Fa-f0-9]{32}')  # 根据自己的需求设置正则
            #             temp = refind.findall(reprval)
            #             stringlist.extend(temp)
    print(f"dong -----------> string list: {stringlist}")
    if len(stringlist) > 0:
        writefile(filename, stringlist)  # 将解析结果和对应的pcap包保存下来


if __name__ == "__main__":
    search('dong.pcap')
