# -*- coding: UTF-8 -*-    
# Author: Dongjd
# FileName: deprecation
# DateTime: 2020/12/14 14:38
# Project: operate_backend_be
# Do Not Touch Me!

from tuoen.sys.core.exception.business_error import BusinessError


class Deprecated(object):
    def __init__(self, cls):
        self.cls = cls

    def __getattr__(self, item):
        exception_msg = 'the {} has been deprecated, so the method can not be accessed.'.format(self.cls.__name__)
        raise BusinessError(exception_msg)

    def __call__(self, *args, **kwargs):
        return self
