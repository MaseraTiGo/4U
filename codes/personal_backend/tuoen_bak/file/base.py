# coding=UTF-8

'''
Created on 2016年8月30日

@author: Administrator
'''

# import python standard package

# import thread package

# import my project package
from api.core.api import APIException
from api.core.api_helper import TokenHelper

from tuoen.service.user.manager import UserServer
from tuoen.utils.potocol.custom_potocol import BaseCustomProtocol
from tuoen.utils.exception.api_error import APIBaseError
from tuoen.utils.exception.business_error import BusinessError


class FileBaseProtocol(BaseCustomProtocol):
    
    def __init__(self, request):
        self.request = request
        self._auth_filed = 'auth_token'
    
    @property
    def parms(self):
        return { key:value for key, value in self.request.POST.items()}
    
    def valid(self):
        if self._auth_filed not in self.parms:
            raise APIException(10007)()

        auth_token = self.parms[self._auth_filed]
        token_helper = TokenHelper(TokenManager.get_token(auth_token))
        if token_helper.is_unvalid :
            raise APIException(10008)()

        if token_helper.is_expire:
            raise APIException(10009)()

        return token_helper.get_auth_user()
    
    def deal(self, request, auth_user):
        """实际处理文件数据的方法"""
        
    def _success(self, result):
        return {'status':1,'data':result} 
    
    def _fail(self, result):
        response_result = {'status':0}
        response_result.update(result) 
        return response_result
    
    def excute(self):
        try:
            auth_user = self.valid()
            result = self.deal(self.request, auth_user)
            return self._success(result if result else "")
        except (APIBaseError, BusinessError) as e:
            return self._fail(e())
        except:
            return self._fail(APIException(10001)()())
