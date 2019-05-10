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

from model.store.model_staff_alias import StaffAlias


class StaffAliasServer(object):

    @classmethod
    def generate(cls, **attr):
        """创建别名"""

        StaffAlias.create(**attr)

    @classmethod
    def get(cls, alias_id):
        """获取别名详情"""

        staff_alias = StaffAlias.get_byid(alias_id)
        if staff_alias is None:
            raise BusinessError("别名不存在")
        return staff_alias

    @classmethod
    def search(cls, current_page, **search_info):
        """查询别名列表"""

        staff_alias_qs = StaffAlias.query(**search_info)

        staff_alias_qs = staff_alias_qs.order_by("-create_time")
        return Splitor(current_page, staff_alias_qs)

    @classmethod
    def is_name_exist(cls, name, staff_alias = None):
        """判断员工别名是否存在"""

        staff_alias_qs = StaffAlias.search(alias = name)

        if staff_alias is not None:
            staff_alias_qs = staff_alias_qs.filter(~Q(id = staff_alias.id))

        if staff_alias_qs.count() > 0:
            raise BusinessError("该名称已存在")
        return True

    @classmethod
    def update(cls, staff_alias, **attrs):
        """编辑别名"""

        staff_alias.update(**attrs)
        return True

    @classmethod
    def remove(cls, alias_id):
        """删除别名"""

        staff_alias = cls.get(alias_id)

        staff_alias.delete()
        return True
