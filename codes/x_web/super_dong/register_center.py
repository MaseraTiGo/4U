# -*- coding: utf-8 -*-
# @File    : register_center
# @Project : djangoProject
# @Time    : 2022/10/12 11:00
"""                     
                                      /             
 __.  , , , _  _   __ ______  _    __/  __ ____  _, 
(_/|_(_(_/_</_/_)_(_)/ / / <_</_  (_/_ (_)/ / <_(_)_
                                                 /| 
                                                |/  
"""

__all__ = ('AdminApiRepo', 'UserApiRepo', 'placeholder')

from super_dong.apis.admin.account.api import Login
from super_dong.apis.admin.money.api import Create, QuickCreate, Details
from super_dong.apis.file_download.api import FileDownload
from super_dong.apis.file_upload.api import FileUpload
from super_dong.frame.core.api_repo import BaseRepo


class AdminApiRepo(BaseRepo):
    SERVICE_NAME = 'admin service'
    SERVICE_TAG = 'admin'
    ACCEPT = 'application/json'
    CONTENT_TYPE = 'application/json'


class UserApiRepo(BaseRepo):
    SERVICE_NAME = 'user service'
    SERVICE_TAG = 'user'
    ACCEPT = 'application/json'
    CONTENT_TYPE = 'application/json'


AdminApiRepo.add(Login)
AdminApiRepo.add(Create)
AdminApiRepo.add(QuickCreate)
AdminApiRepo.add(Details)


class FileDownloadRepo(BaseRepo):
    SERVICE_NAME = 'file download'
    SERVICE_TAG = 'file_download'
    ACCEPT = 'application/json'
    CONTENT_TYPE = 'application/octet-stream'


FileDownloadRepo.add(FileDownload)


class FileUploadRepo(BaseRepo):
    SERVICE_NAME = 'file upload'
    SERVICE_TAG = 'file_upload'
    ACCEPT = 'multipart/form-data'
    CONTENT_TYPE = 'application/json'


FileUploadRepo.add(FileUpload)


def placeholder():
    pass
