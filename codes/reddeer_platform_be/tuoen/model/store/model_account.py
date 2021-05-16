# coding=UTF-8

'''
Created on 2016年7月22日

@author: Administrator
'''

from django.db.models import *
from django.utils import timezone

from model import AGENT_PREFIX, PLATFORM_PREFIX
from model.base import BaseModel
from model.fields import VirtualForeignKey
from model.store.model_company import Company
from model.store.model_role import AgentRole, PlatformRole


class MyManager(Manager):
    def get_queryset(self):
        super_qs = super().get_queryset()
        return super_qs.exclude(status=BaseAccount.Status.DELETE)


class BaseAccount(BaseModel):
    """基础账号表"""

    class Status(IntegerChoices):
        DISABLE = 0
        ENABLE = 1
        DELETE = 2

        # STATUS_CHOICES = [(ENABLE, '启用'), (DISABLE, "停用")]

    username = CharField(verbose_name="账号", max_length=32)
    password = CharField(verbose_name="密码", max_length=64)
    name = CharField(verbose_name="姓名", max_length=32, default='')
    phone = CharField(verbose_name="联系电话", max_length=24, default='')
    status = IntegerField(verbose_name="账号状态状态:DISABLE = 0 ENABLE = 1 DELETE = 2 "
                                       "[(ENABLE, 启用), (DISABLE, 停用), (DELETE, 删除)]",
                          choices=Status.choices, default=Status.ENABLE)
    last_login_time = DateTimeField(verbose_name="最后一次登录时间", default=timezone.now)

    objects = MyManager()

    class Meta:
        abstract = True


class PlatformAccount(BaseAccount):
    """B端账号表"""

    role = VirtualForeignKey(PlatformRole, on_delete=CASCADE, related_name='role_platform_accounts')
    is_main = BooleanField(verbose_name='是否为主账号', default=False)

    class Meta:
        db_table = PLATFORM_PREFIX + 'account'


class AgentAccount(BaseAccount):
    """A端账号表"""

    role = VirtualForeignKey(AgentRole, on_delete=CASCADE, related_name='role_agent_accounts')
    company = VirtualForeignKey(Company, on_delete=CASCADE, related_name='agent_accounts')
    is_main = BooleanField(verbose_name='是否为主账号', default=False)

    class Meta:
        db_table = AGENT_PREFIX + 'account'
