# coding=UTF-8

'''
Created on 2016年7月27日

@author: Administrator
'''

SYS_ERROR_CODES = (
                (10001, '系统错误'),
                (10002, '请求的接口不存在'),
                (10003, '请求频率超过上限'),
                (10004, '请求接口超过时效性'),
                (10005, '缺失公共参数(%s),请参考API文档'),
                (10006, '请求数据被篡改'),
                (10007, '不能缺少(auth_token)参数'),
                (10008, 'auth_token不存在'),
                (10009, 'auth_token已过期,请重新获取'),
              )

SERVER_ERROR_CODES = (
                        (20001, "账号或密码错误"),
                        (20002, "缺失必选参数(%s),请参考API文档"),
                        (20003, "参数(%s)值非法，请参考API文档"),
                      )

BUSINESS_ERROR_CODES = (30001,)