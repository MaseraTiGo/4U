# coding=UTF-8

'''
Created on 2016-7-4

@author: YRK
'''


from tuoen.utils.exception.base import BaseError
from tuoen.utils.exception.error_code import BUSINESS_ERROR_CODES

class BusinessError(BaseError):
    
    code = BUSINESS_ERROR_CODES[0]
    
    def __init__(self,msg):
        self.msg = msg

    def __str__(self):
        return "【{code}】{msg}".format(code = self.code, msg = self.msg)

    def __call__(self):
        return {"code":self.code, "msg":self.msg}

business_manager = BusinessError

