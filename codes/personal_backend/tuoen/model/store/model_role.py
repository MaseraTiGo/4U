# coding=UTF-8

'''
Created on 2016年7月22日

@author: Administrator
'''

import json
from django.db.models import *
from django.utils import timezone
from model.base import BaseModel


class Role(BaseModel):
    name = CharField(verbose_name = "角色名称", max_length = 64, default = "")
    parent_id = IntegerField(verbose_name = "对应上级角色id", default = 0)
    rules = TextField(verbose_name = "角色对应权限", default = "[]")
    describe = TextField(verbose_name = "描述", default = "")
    is_show_data = BooleanField(verbose_name = "是否展示下级数据", default = True)
    is_show_all = BooleanField(verbose_name = "是否展示所有数据(类admin)", default = False)
    is_security = BooleanField(verbose_name = "是否隐藏关键信息(安全)", default = True)
    status = BooleanField(verbose_name = "状态", default = True)
    update_time = DateTimeField(verbose_name = "更新时间", auto_now = True)
    create_time = DateTimeField(verbose_name = "创建时间", default = timezone.now)

    @classmethod
    def search(cls, **attrs):
        role_qs = cls.query().filter(**attrs)
        return role_qs

    @property
    def rule_list(self):
        try:
            return json.loads(self.rules)
        except Exception as e:
            print(e)
            return []
