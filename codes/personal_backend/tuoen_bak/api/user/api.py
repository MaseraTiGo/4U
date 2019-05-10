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

from tuoen.api.user.token import *
from tuoen.api.user.verifycode import *
from tuoen.api.user.customer import *


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


@api_register(PatientServer, DoctorServer)
def updatepsd(auth_user, phone, verify_code, new_passwd):
    """
        @author: yrk
        @version: 1.0

        @desc : 修改密码

        @param : phone (string) # 手机号
        @param : verify_code (string) # 短信验证码
        @param : new_passwd (string) # 加密过的密码，加密方式为（md5）

        @return
            success : {
                status : 1 (int) # 系统调用OK，无异常出现
                data :""
            }

            fail : {
                status : 0 (int) # 系统调用OK，无异常出现
                msg : "xxxxxxxx" # 系统错误消息
                code : 10001 # 系统错误code
            }
    """

    return None


@api_register(PatientServer, DoctorServer, OrganizationServer)
def bindphone(auth_user, phone, verify_code, passwd):
    """
        @author: yrk
        @version: 1.0

        @desc : 修改绑定手机号

        @param : phone (string) # 手机号
        @param : verify_code (string) # 短信验证码
        @param : passwd (string) # 加密过的密码，加密方式为（md5）

        @return
            success : {
                status : 1 (int) # 系统调用OK，无异常出现
                data :""
            }

            fail : {
                status : 0 (int) # 系统调用OK，无异常出现
                msg : "xxxxxxxx" # 系统错误消息
                code : 10001 # 系统错误code
            }
    """

    return None


@api_register(PatientServer, DoctorServer, is_auth=False)
def forgetpsd(phone, verify_code, new_passwd, role_type):
    """
        @author: yrk
        @version: 1.0

        @desc : 找回密码

        @param : phone (string) # 手机号 (注册手机号)
        @param : verify_code (string) # 短信验证码
        @param : new_passwd (string) # 加密过的密码，加密方式为（md5）
        @param : role_type (int) # 0、用户 端 1、医生端

        @return
            success : {
                status : 1 (int) # 系统调用OK，无异常出现
                data :""
            }

            fail : {
                status : 0 (int) # 系统调用OK，无异常出现
                msg : "xxxxxxxx" # 系统错误消息
                code : 10001 # 系统错误code
            }
    """

    return None


@api_register(PatientServer, is_auth=False)
def verify(phone, verify_code, role_type):
    """
        @author: yrk
        @version: 微信端

        @desc : 验证验证码和用户

        @param : phone (string) # 手机号 (注册手机号)
        @param : verify_code (string) # 短信验证码
        @param : role_type (int) # 0、用户 端 1、医生端

        @return
            success : {
                status : 1 (int) # 系统调用OK，无异常出现
                data :""
            }

            fail : {
                status : 0 (int) # 系统调用OK，无异常出现
                msg : "xxxxxxxx" # 系统错误消息
                code : 10001 # 系统错误code
            }
    """

    return True
