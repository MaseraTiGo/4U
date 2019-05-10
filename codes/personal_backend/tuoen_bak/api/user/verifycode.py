# coding=UTF-8

'''
Created on 2016年7月29日

@author: Administrator
'''

# import python standard package

# import thread package

# import my project package
from tuoen.api.core.api_helper import api_register
from tuoen.api.core.api_server import PatientServer, DoctorServer, OrganizationServer


@api_register(PatientServer, DoctorServer, OrganizationServer, is_auth=False)
def get(phone, code_type):
    """
        @author: yrk
        @version: 1.0

        @desc : 获取短信验证码

        @param : phone (string) # 注册电话
        @param : code_type (string) # 短信类型
            enum types :
                register - 注册短信,
                modify_phone - 修改手机号短信,
                modify_passwd - 修改密码短信,
                forget_passwd - 忘记密码短信,

        @return
            success : {
                status : 1 (int) # 系统调用OK，无异常出现
                data : {
                    verify_code: # 验证码
                }
            }

            fail : {
                status : 0 (int) # 系统调用OK，无异常出现
                msg : "xxxxxxxx" # 系统错误消息
                code : 10001 # 系统错误code
            }
    """

    return {"verify_code": '123456'}
