# coding=UTF-8

'''
Created on 2016年7月26日

@author: Administrator
'''
from tuoen.api.core.api_helper import api_register
from tuoen.api.core.api_server import PatientServer, DoctorServer, CrmServer
from tuoen.utils.exception.api_error import error_manager


@api_register(PatientServer, DoctorServer, CrmServer, is_auth=False)
def renewal(auth_token, renewal_flag):
    """
        @author: yrk
        @version: 1.0

        @desc : token续约

        @param : auth_token (string) # 用户最后一次使用的token
        @param : renewal_flag (string) # 用户用于续约的标识，该标示会在登陆后，或每次续约后自动更换

        @return
            success : {
                status : 1 (int) # 系统调用OK，无异常出现
                data : {
                    "renewal_flag":token.renewal_flag, # 重置token标示
                    "auth_token":token.auth_token, # 访问token
                    "expire_time":token.expire_time, # 过期时间
                }
            }

            fail : {
                status : 0 (int) # 系统调用OK，无异常出现
                msg : "xxxxxxxx" # 系统错误消息
                code : 10001 # 系统错误code
            }
    """

    raise error_manager.get_error(10007)
