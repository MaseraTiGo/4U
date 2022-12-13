# -*- coding: utf-8 -*-
# @File    : __init__.py
# @Project : hitler_adolf
# @Time    : 2022/6/6 16:25
"""                     
                                      /             
 __.  , , , _  _   __ ______  _    __/  __ ____  _, 
(_/|_(_(_/_</_/_)_(_)/ / / <_</_  (_/_ (_)/ / <_(_)_
                                                 /| 
                                                |/  
"""

import logging


def my_logger(name='SuperDong', log_path='logs/cmd_record.log'):

    logger = logging.getLogger(f'[{name}]')

    f_handler = logging.FileHandler(log_path)

    f_handler.setLevel(logging.INFO)

    f_format = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    f_handler.setFormatter(f_format)

    logger.addHandler(f_handler)
    return logger


superDong = my_logger()
