# coding=UTF-8

'''
Created on 2016年7月22日

@author: Administrator
'''
import time
import hashlib
import datetime
import json
import random

from django.db.models import *

from tuoen.sys.core.exception.business_error import BusinessError
from tuoen.sys.utils.common.split_page import Splitor

from model.models import Role, AuthAccess

from tuoen.abs.middleware.role import role_middleware


class RoleHelper(object):

    @classmethod
    def generate(cls, **role_info):
        """创建角色"""

        role = Role.create(**role_info)
        if role is None:
            raise BusinessError("角色创建失败")

        role_middleware.force_refresh()
        return role

    @classmethod
    def search(cls, **attrs):
        """查询角色列表"""
        role_list = Role.search(**attrs)
        return role_list

    @classmethod
    def get(cls, role_id):
        """获取角色详情"""
        role = Role.get_byid(role_id)
        if role is None:
            raise BusinessError("该角色不存在")
        return role

    @classmethod
    def update(cls, role, **attrs):
        """编辑角色"""
        role.update(**attrs)
        time_start = time.time()
        role_middleware.force_refresh()
        time_end = time.time()
        print("====结束时间====", time_end)
        print("====相差时间====", time_end - time_start)
        return True

    @classmethod
    def remove(cls, role_id):
        """删除角色"""
        access_type = "role"
        auth_access = AuthAccess.get_by_access_id(role_id, access_type)
        if auth_access.count() > 0:
            raise BusinessError("已绑定用户无法删除")

        role_children = role_middleware.get_children(role_id)
        if role_children:
            raise BusinessError("此角色存在下级无法删除")

        role = Role.get_byid(role_id)
        if role is None:
            raise BusinessError("此角色不存在")

        role.delete()
        role_middleware.force_refresh()
        return True

    @classmethod
    def is_exit(cls, role_id):
        """判断该角色是否存在"""
        role = Role.get_byid(role_id)
        if role is None:
            return False
        return True

    @classmethod
    def is_name_exist(cls, name, role = None):
        """判断角色名称是否存在"""
        role_qs = Role.search(name = name)

        if role is not None:
            role_qs = role_qs.filter(~Q(id = role.id))

        if role_qs.count() > 0:
            raise BusinessError("该名称已存在")
        return True
