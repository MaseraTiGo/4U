# coding=UTF-8

'''
Created on 2016年8月30日

@author: Administrator
'''

# import python standard package

# import my project package

# import thread package

from .base import FileBaseProtocol

class UploadFileProtocol(FileBaseProtocol):
    
    def deal(self, request, auth_user):
        file = request.FILES.get('upload_file')
        bucket_name = request.POST.get("store_type")
        print("执行存储图片操作....")
        return {'url':""}
