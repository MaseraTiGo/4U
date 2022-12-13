# -*- coding: utf-8 -*-
# @File    : api
# @Project : djangoProject
# @Time    : 2022/10/13 10:06
"""                     
                                      /             
 __.  , , , _  _   __ ______  _    __/  __ ____  _, 
(_/|_(_(_/_</_/_)_(_)/ / / <_</_  (_/_ (_)/ / <_(_)_
                                                 /| 
                                                |/  
"""
import time

from super_dong.frame.core.api import AuthApi
from super_dong.frame.core.data_field import FileField, CharField
from super_dong.frame.core.data_field.data_type import ResponseData


class FileDownload(AuthApi):
    class File(ResponseData):
        file_path = FileField(verbose='my file')
        file_name = CharField(verbose='aston.pdf', max_length=-1)

    @classmethod
    def get_desc(cls):
        pass

    @classmethod
    def get_author(cls):
        pass

    @classmethod
    def get_history(cls):
        pass

    @classmethod
    def get_unique_num(cls):
        pass

    def execute(self):
        return 'logic_book.pdf'

    def tidy(self, book):
        return {
            'File': {
                'file_path': book,
                'file_name': f'aston_{time.time_ns()}.pdf'
            }
        }
