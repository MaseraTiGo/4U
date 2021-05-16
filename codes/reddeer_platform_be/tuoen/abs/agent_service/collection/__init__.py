# -*- coding: UTF-8 -*-    
# Author: Dongjd
# FileName: __init__.py
# DateTime: 2020/12/15 16:04
# Project: awesome_dong
# Do Not Touch Me!

import enum


class ExportType(enum.IntEnum):
    EXCEL_ONLY = 1
    ATTACHMENT_ONLY = 2
    EXCEL_AND_ATTACHMENT = 3


class AttachmentExportType(enum.IntEnum):
    BY_QUESTION = 1
    BY_CUSTOMER = 2
