# coding=UTF-8

'''
Created on 2016年7月22日

@author: Administrator
'''

from django.db.models import *
from django.utils import timezone
from model.base import BaseModel
from model.store.model_user import Staff


class StatusType(object):
    ENABLE = 'enable'
    LOCK = 'lock'
    DISABLE = 'disable'
    NOTACTIVE = 'notactive'

    CHOICES = ((ENABLE, '启用'), (NOTACTIVE, '待激活'), (LOCK, "锁定"), (DISABLE, "禁用"))


class BaseAccount(BaseModel):
    """基础账号表"""
    username = CharField(verbose_name="账号", max_length=64)
    password = CharField(verbose_name="密码", max_length=64)
    last_login_time = DateTimeField(verbose_name="最后一次登录时间", null=True, blank=True)
    last_login_ip = CharField(verbose_name="最后一次登录ip", max_length=64, default='')
    register_ip = CharField(verbose_name="注册IP", max_length=64, default='')
    status = CharField(verbose_name="账号状态", max_length=64, choices=StatusType.CHOICES, default=StatusType.NOTACTIVE)
    update_time = DateTimeField(verbose_name="更新时间", auto_now=True)
    create_time = DateTimeField(verbose_name="创建时间", default=timezone.now)

    class Meta:
        abstract = True

    @classmethod
    def get_account_byusername(cls, username):
        """ 根据用户名查询账号信息 """
        try:
            return cls.objects.filter(username=username)[0]
        except:
            return None


class StaffAccount(BaseAccount):
    """员工账号表"""
    staff = ForeignKey(Staff, on_delete=CASCADE)

    @classmethod
    def create_byadmin(cls, **kwargs):
        staff = Staff.create(**kwargs)
        if staff is None:
            return None
        kwargs.update({'staff': staff})
        return super(BaseAccount, cls).create(**kwargs)

    @classmethod
    def get_account_bystaff(cls, staff_id):
        """根据staff_id查询账号信息"""
        try:
            return cls.objects.filter(staff=staff_id)[0]
        except:
            return None
