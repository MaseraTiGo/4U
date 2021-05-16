# coding=UTF-8
import time
import random
import re


def generate_sn(prefix):
    """生成订单号"""
    rand_num = str(random.randint(1000, 9999))
    time_mark = str(int(time.time() * 1000))
    sn = prefix + time_mark + rand_num
    return sn


def filter_emoji(desstr, restr=''):
    """过滤emoji"""
    try:
        co = re.compile(u'[\U00010000-\U0010ffff]')
    except re.error:
        co = re.compile(u'[\uD800-\uDBFF][\uDC00-\uDFFF]')
    return co.sub(restr, desstr)
