# -*- coding: UTF-8 -*-    
# Author: Dongjd
# FileName: __init__.py
# DateTime: 1/28/2021 5:09 PM
# Project: awesome_dong
# Do Not Touch Me!

from collections import namedtuple

from .std_excel_template import StdExcelTemplate

ExcelTemplate = namedtuple('ExcelTemplates', 'name unique_num')

std_excel = ExcelTemplate(StdExcelTemplate.NAME, StdExcelTemplate.UNIQUE_NUM)

templates_mapping = {
    StdExcelTemplate.UNIQUE_NUM: StdExcelTemplate
}

template_tuple_list = [std_excel]
