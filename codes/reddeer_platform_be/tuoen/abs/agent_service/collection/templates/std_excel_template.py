# -*- coding: UTF-8 -*-    
# Author: Dongjd
# FileName: std_excel_template
# DateTime: 2/1/2021 11:47 AM
# Project: awesome_dong
# Do Not Touch Me!

import random
from string import ascii_letters

from .base import BaseExcelTemplate


def generate_test_data(num=10):
    return [[''.join(random.sample(ascii_letters, 6)) for _ in range(6)] for _ in range(num)]


class StdExcelTemplate(BaseExcelTemplate):
    NAME = '标准excel导出样式'
    UNIQUE_NUM = 1001
