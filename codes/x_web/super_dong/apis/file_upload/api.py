# -*- coding: utf-8 -*-
# @File    : api
# @Project : djangoProject
# @Time    : 2022/10/13 10:51
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
from super_dong.frame.core.data_field.data_type import RequestData, ResponseData


class FileUpload(AuthApi):
    class File(RequestData):
        files = FileField(verbose='my file')

    class Yes(ResponseData):
        msg = CharField(verbose='msg', max_length=-1)

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
        for _, neo in self.File.files.items():
            try:
                with open(f'dong_aston_{time.time_ns()}.pdf', "wb") as f:
                    for chunk in neo.chunks():
                        f.write(chunk)
            except IOError as e:
                raise Exception(f"文件保存失败:{e}")
        return 'mother fucker'

    def tidy(self, msg):
        return {
            'Yes': {
                'msg': msg
            }
        }
