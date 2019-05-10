# coding=UTF-8

'''
Created on 2016年7月22日

@author: Administrator
'''

from django.db.models import *
from model.base import BaseModel


class RoleType(object):
    CUSTOMER = 0
    DOCTOR = 1
    EMPLOYEE = 10
    STAFF = 99
    CHOICES = ((CUSTOMER, '用户角色'), (DOCTOR, "医生角色"),\
               (EMPLOYEE, "第三方检测机构员工"), (STAFF, "员工角色"))


class SourceType(object):
    UNKNOWN = "unknow"
    APP_STORE = "app_store"
    TSZ = "360"
    NO = "91"
    ANZHI = "anzhi"
    BAIDU = "baidu"
    FLYME = "flyme"
    OPPO = "oppo"
    QQ = "qq"
    UC = "uc"
    XIAOMI = "xiaomi"
    WEB = "web"

    CHOICES = ((TSZ, '360'), (NO, "91"), (ANZHI, "安智"), (BAIDU, "百度"),\
               (FLYME, "魅族"), (OPPO, "oppo"), (QQ, "qq"), (UC, "uc"),\
                (XIAOMI, "小米"), (WEB, "网站"), (APP_STORE, "苹果商店"),\
                 (UNKNOWN, '未知'))


class PlatformType(object):
    UNKNOWN = 0
    ANDROID = 1
    IOS = 2
    CRM = 3
    ORGANIZATION = 3

    CHOICES = ((UNKNOWN, '未知'), (ANDROID, 'android'), (IOS, 'iphone'), (CRM, 'crm'), (ORGANIZATION, 'organization'))


class User(BaseModel):
    """用户基础验证表"""
    account = CharField(verbose_name="账号", max_length=64)
    passwd = CharField(verbose_name="密码", max_length=64)
    phone = CharField(verbose_name="手机号", max_length=20)
    role_type =IntegerField(verbose_name="角色类型", choices=RoleType.CHOICES)

    nick = CharField(verbose_name="昵称", max_length=64, default="")
    photo_url = CharField(verbose_name="头像", max_length=256, default="")

    last_login = DateTimeField(verbose_name="最后一次登录时间", auto_now_add=True)
    last_version = CharField(verbose_name="最后一个版本信息", max_length=32, default="2.0.1")
    last_platform = CharField(verbose_name="最后一次的平台信息", max_length=32, default="")

    plat_type = IntegerField(verbose_name="注册平台", choices=PlatformType.CHOICES, default=PlatformType.UNKNOWN)
    source = CharField(verbose_name="来源", max_length=32, choices=SourceType.CHOICES, default=SourceType.UNKNOWN)
    update_time = DateTimeField(verbose_name="更新时间", auto_now=True)
    create_time = DateTimeField(verbose_name="创建时间", auto_now_add=True)

    @classmethod
    def get_user_byaccount(cls, phone, role_type):
        try:
            return cls.objects.filter(Q(account=phone) | Q(phone=phone)).\
                filter(role_type=role_type)[0]
        except:
            return None
