# coding=UTF-8

'''
Created on 2016年7月22日

@author: Administrator
'''

import hashlib
import datetime
import json
import random

from django.db.models import *

from tuoen.sys.core.exception.business_error import BusinessError
from tuoen.sys.utils.common.split_page import Splitor
from model.store.model_account import StatusType
from model.store.model_journal import JournalTypes, OperationTypes
from model.models import StaffAccount
from tuoen.abs.middleware.journal import JournalMiddleware


class StaffAccountServer(object):

    @classmethod
    def register(cls, **attrs):
        """创建员工"""
        attrs.update({'password': hashlib.md5("123456".encode("utf-8")).hexdigest()})
        account = StaffAccount.create_byadmin(**attrs)
        if account is None:
            raise BusinessError("员工创建失败")
        return account

    @classmethod
    def register_account_bystaff(cls, staff, ip, **account_info):
        """给员工添加账号或修改账号"""
        account_qs = StaffAccount.query(staff = staff)
        if account_qs.count() > 0:
            account = account_qs[0]
            check_username_qs = StaffAccount.query().filter(username = account_info["username"]).filter(~Q(id = account.id))
            if check_username_qs.count() > 0:
                raise BusinessError("该账号已存在")
            account.update(**account_info)
        else:
           if cls.get_account_byusername(account_info["username"]):
               if 'password' not in account_info:
                   raise BusinessError("密码不能为空")
               account = StaffAccount.create(username = account_info["username"], password = account_info["password"], \
                                             register_ip = ip, staff = staff, status = account_info["status"])

        return account

    @classmethod
    def login(cls, username, password, ip):
        """员工登录"""
        account = StaffAccount.get_account_byusername(username)
        if account is None:
            raise BusinessError("账号或密码错误")

        if password != account.password:
            raise BusinessError("账号或密码错误")

        if account.status == StatusType.LOCK:
            raise BusinessError("该账号已被锁定")

        if account.status == StatusType.DISABLE:
            raise BusinessError("该账号已被禁用")

        account.update(last_login_time = datetime.datetime.now(), status = StatusType.ENABLE)
        record_detail = "{who} 在 {datetime} 登录了系统，登陆 ip: {ip}".format(who = account.staff.name, datetime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), ip = ip)
        remark = "登录系统"
        JournalMiddleware.register(account.staff, OperationTypes.STAFF, account.staff, \
                       OperationTypes.STAFF, JournalTypes.LOGIN, record_detail, remark)
        return account

    @classmethod
    def update(cls, account, **attrs):
        """修改账号信息"""
        account.update(**attrs)
        return account

    @classmethod
    def get_account_bystaff(cls, staff):
        """根据员工获取账号对象"""
        account_qs = StaffAccount.query(staff = staff)
        if account_qs.count() == 0:
            raise BusinessError("账号不存在")
        return account_qs[0]

    @classmethod
    def get_account_byusername(cls, username):
        """根据用户名判断账号对象是否存在"""
        account = StaffAccount.get_account_byusername(username = username)
        if account is not None:
            raise BusinessError("该账号已存在")
        return True

    @classmethod
    def modify_password(cls, account, password, newpassword):
        """修改员工密码"""
        if password != account.password:
            raise BusinessError("原密码错误")
        account.update(password = newpassword)
        return True

    @classmethod
    def search(cls, current_page):
        """查询账号列表"""
        account_list = StaffAccount.query()
        return Splitor(current_page, account_list)

    @classmethod
    def hung_account_forstaffs(cls, staff_list):
        """员工列表挂载账号信息"""
        staff_mapping = {}
        for staff in staff_list:
            staff_mapping[staff.id] = staff
            staff.account = None

        account_list = StaffAccount.query(staff__in = staff_mapping.keys())

        for account in account_list:
            if account.staff.id in staff_mapping:
                staff_mapping[account.staff.id].account = account
        return staff_list

    @classmethod
    def generate_accout_bystaff(cls, username, staff):
        """根据员工生成账号"""
        password = hashlib.md5("123456".encode("utf-8")).hexdigest()
        account = StaffAccount.create(username = username, password = password, staff = staff)
        if account is None:
            raise BusinessError("账号创建失败")
        return account
