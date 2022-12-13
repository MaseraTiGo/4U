# -*- coding: utf-8 -*-
# @File    : settings
# @Project : hitler_adolf
# @Time    : 2022/6/6 16:25
"""                     
                                      /             
 __.  , , , _  _   __ ______  _    __/  __ ____  _, 
(_/|_(_(_/_</_/_)_(_)/ / / <_</_  (_/_ (_)/ / <_(_)_
                                                 /| 
                                                |/  
"""

REDIS_CONF = {
    # 'host': '192.168.200.151',
    'host': '192.168.200.152',
    'port': '6379',
    'max_connections': 100,
    'db': 5,
    'password': 'aston-martin'
}

KEY_EXPIRE = 10

RECORD_CMD_SWITCH = True

MY_PREFIX = 'superDong ------------------>'

# listeners
LISTENERS = [
    'executioner'
]

# services
SERVICES = [
    #'board_of_punishments'
]

AMQP_URI_CONF = {
    'AMQP_URI': 'pyamqp://stackrabbit:cykj1235@192.168.202.247:5672'
}
