# coding=UTF-8

'''
Created on 2016-7-4

@author: YRK
'''

from tuoen.sys.core.exception.base import BaseError


class AccessCodes(object):
    ACCESS_LIMIT = 50001
    FORBIDDEN = 50002


class AccessLimitError(BaseError):
    code = AccessCodes.ACCESS_LIMIT
    desc = "访问限制"


class AccountForbiddenError(BaseError):
    code = AccessCodes.FORBIDDEN
    desc = '账户被停用'
