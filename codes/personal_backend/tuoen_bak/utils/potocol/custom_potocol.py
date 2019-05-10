# coding=UTF-8

'''
Created on 2016年7月23日

@author: Administrator
'''

import json

class BaseCustomProtocol(object):
    """自定义协议基类 """

    def decode(self, data):
        """解密"""
        return data

    def valid(self):
        """验证用户是否有效"""
        return True

    def check(self):
        """调用业务前的检查"""
        return True

    def serialize(self, data):
        """序列化"""
        return json.dumps(data)

    def encrypt(self, data):
        """加密（可以包含混淆操作）"""
        return data