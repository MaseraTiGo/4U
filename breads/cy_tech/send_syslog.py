# -*- coding: utf-8 -*-
# @File    : send_syslog
# @Project : 4U
# @Time    : 2024/7/17 15:48
# once, I want 2 leave my name 2 the history
# sadly, I find that my hair gets pale
"""                     
                                      /             
 __.  , , , _  _   __ ______  _    __/  __ ____  _, 
(_/|_(_(_/_</_/_)_(_)/ / / <_</_  (_/_ (_)/ / <_(_)_
                                                 /| 
                                                |/  
"""
import sys
import zmq
import time

IP_ADDRESS = "127.0.0.1"
ZMQ_LOG_DATA_RECEIVER = f"tcp://{IP_ADDRESS}:5804"

LOG_MESSAGES = {
    "template": "{\"log\":\"[IFWv2][POLICY][INDU-TEMPLATE][NOTICE]:LEN=10240 ID=21785 SRC=192.168.200.63 DST=58.49.157.165 PROTO=tcp SP=42735 DP=443 ACTION=DROP ID=1\"}",
    "limit0": "{\"log\":\"[IFWv2][OPT][LIMIT][LEVEL]:USER=user UIP=ip CONTENT=\\\"编辑时间对象成功: 名字：fasd-->fasd，内容：2022-04-12 14:21 - 2022-04-26 00:00-->2022-04-12 14:46 - 2022-04-26 00:00 \\\" RET=1\"}",
    "industrialtemp": "{\"log\":\"[IFWv2][OPT][INDUSTRIALTEMP][INFO]:USER=operator UIP=192.168.100.39 CONTENT=\\\"opc模板启用成功\\\" RET=23\"}",
    "inds": "{\"log\":\"[IFWv2][POLICY][INDS][INFO]:LEN=77 ID=57113 SRC=217.12.10.62 DST=172.26.0.4 PROTO=tcp SP=110 DP=34976 ALPROTO=pop3 DETAIL=interface:xxx,method:xxx  ACTION=ACCEPT RID=10000171 SID=10000171 ACLID=3 GID=65798144\"}",
    "limit": "{\"log\":\"[IFWv2][POLICY][LIMIT][NOTICE]:LEN=4 ID=2 SRC=5.5.5.5 DST=6.6.6.6 PROTO=tcp SP=234 DP=2324 ACTION=DROP RID=1\"}",
    "ips": "{\"log\":\"[IFWv2][SEC][IPS][CRIT]:LEN=4 ID=2 SRC=1.1.1.1 DST=2.2.2.2 PROTO=udp SP=33 DP=5664 ATYPE= AMETH= RISK=MID ACTION=DROP RID=100000 ACLID=1\"}",
    "nat": "{\"log\":\"[IFWv2][NAT][PAT][INFO]:LEN=5 ID=3 SRC=192.168.200.63 DST=52.109.88.39 PROTO=tcp SP=27851 DP=443 NTYPE=SNAT NADDR=192.168.100.64 NPORT=27851 RID=1\"}",
    "system": "{\"log\":\"[IFWv2][SYS][SYSTEM][CRIT]:CONTENT=\\\"你好啊这个世界是什么样的恩\\\"\"}",
    "defend": "{\"log\":\"[IFWv2][SEC][DEFEND][ALERT]:LEN=63 ID=66 SRC=192.168.200.63 DST=192.168.50.65 PROTO=tcp SP=1122 DP=139 ATYPE=DOS AMETH=WINNUKE RISK=HIGH ACTION=DROP\"}",
    "session": "{\"log\":\"[IFWv2][SESSION][FLOW][INFO]:LEN=10240 ID=21785 SRC=192.168.200.63 DST=58.49.157.165 PROTO=tcp SP=42735 DP=443\"}",
    "policy": "{\"log\":\"[IFWv2][POLICY][INDS][INFO]:LEN=77 ID=57113 SRC=217.12.10.62 DST=172.26.0.4 PROTO=tcp SP=110 DP=34976 ALPROTO=pop3 DETAIL=interface:xxx,method:xxx  ACTION=ACCEPT RID=10000171 SID=10000171 ACLID=3 GID=65798144\"}",
    "vul": "{\"log\":\"[IFWv2][SEC][IPS][CRIT]:LEN=4 ID=2 SRC=1.1.1.1 DST=2.2.2.2 PROTO=udp SP=33 DP=5664 ATYPE= AMETH= RISK=MID ACTION=DROP RID=100000 ACLID=1\"}",
    "ipmac": "{\"log\":\"[IFWv2][POLICY][MACIP][NOTICE]:LEN=4 ID=2 SRC=5.5.5.5 DST=6.6.6.6 PROTO=tcp SP=234 DP=2324 SMAC= 00:90:0b:71:e1:2d DMAC= 00:90:0b:71:e1:2c ACTION=DROP RID=1\"}",
    "sec": "{\"log\":\"[IFWv2][POLICY][FILTER][INFO]:LEN=1430 ID=2345 SRC=192.168.100.26 DST=192.168.10.80 PROTO=tcp SP=60445 DP=80 ALPROTO=http ACTION=ACCEPT RID=34 PORTIN=eth0 PORTOUT=eth1 SRCMAC=00:90:0b:62:b0:ba DSTMAC=0c:73:eb:93:0d:dc\"}",
}

def main():
    if len(sys.argv) < 2:
        print("Please provide a log type as an argument")
        return

    log_type = sys.argv[1]
    log_num = 10
    if len(sys.argv) == 3:
        try:
            log_num = int(sys.argv[2])
        except ValueError:
            print("Invalid number provided")

    context = zmq.Context()
    socket = context.socket(zmq.PUB)
    socket.bind(ZMQ_LOG_DATA_RECEIVER)
    time.sleep(1)

    msg = LOG_MESSAGES.get(log_type)
    if msg is None:
        print("Unknown log type")
        return

    start_time = time.time()
    for i in range(log_num):
        socket.send_string(msg)
        print(f"send msg ===> {i}")
        # time.sleep(1)

    end_time = time.time()
    cost_time = end_time - start_time
    print(f"{cost_time} seconds==============")
    print("send over")

if __name__ == "__main__":
    main()
