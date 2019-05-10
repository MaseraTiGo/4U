# coding=UTF-8

'''
Created on 2016年7月23日

@author: Administrator
'''

import json
import random
import datetime

# Create your views here.
from tuoen.api.core.api_helper import api_register
from tuoen.api.core.api_server import PatientServer, DoctorServer, OrganizationServer
from tuoen.utils.exception.business_error import BusinessError

from tuoen.service.user.manager import UserServer, CustomerServer

@api_register(PatientServer, DoctorServer, is_auth=False)
def register_notice(role_type):
    """
        @author: yrk
        @version: 1.0

        @desc : 注册须知url

        @param : role_type (int) # 0、用户 端 1、医生端

        @return
            success : {
                status : 1 (int) # 系统调用OK，无异常出现
                data : { url : # 注册须知url}
            }

            fail : {
                status : 0 (int) # 系统调用OK，无异常出现
                msg : "xxxxxxxx" # 系统错误消息
                code : 10001 # 系统错误code
            }
    """

    return {'url': "http://www.baidu.com"}


@api_register(PatientServer, DoctorServer, is_auth=False)
def register(phone, verify_code, passwd, role_type, plat_type=1,\
                 source="web", other_infos=None):
    """
        @author: yrk
        @version: 1.0

        @desc : 注册用户接口

        @param : phone (string) # 注册电话
        @param : verify_code (string) # 注册验证码
        @param : passwd (string) # 加密过的密码，加密方式为（md5）
        @param : role_type (int) # 0、用户 端 1、医生端  99、员工
        @param : plat_type (int-选填) # 1、android 2、ios
        @param : source (string-选填) # 来源，如：web，xiaomi等

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

    role_type = int(role_type)
    other_infos = json.loads(other_infos) if other_infos is not None else {}

    customer, user = CustomerServer.register(phone, verify_code, passwd, role_type,\
                 plat_type, source, **other_infos)
    token = UserServer.make_token(user)
    return token.json()


@api_register(PatientServer, is_auth=False)
def login(phone, passwd, role_type, version='2.0.1', platform=""):
    """
        @author: yrk
        @version: 1.0

        @desc : 登陆接口

        @param : phone (string) # 注册电话
        @param : passwd (string) # 加密过的密码，加密方式为（md5）
        @param : role_type (int) # 0、用户 端 1、医生端  99、员工
        @param : version (string - 选参) # 当前版本
        @param : platform (string - 选参) # 当前平台

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

    user, token = UserServer.login(phone, passwd)
    return token.json()
