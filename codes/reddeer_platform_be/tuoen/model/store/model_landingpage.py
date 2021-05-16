# coding=UTF-8

'''
Created on 2016年7月22日

@author: Administrator
'''

from django.db.models import *

from model import AGENT_PREFIX
from model.base import BaseModel
from model.fields import VirtualForeignKey
from model.store.model_company import Company
from model.store.model_account import AgentAccount
from model.store.utils import generate_uuid


class MyManager(Manager):
    def get_queryset(self):
        super_qs = super().get_queryset()
        return super_qs.exclude(status=LandingPage.Status.DELETE)


class MyAllManager(Manager):
    ...


class LandingPage(BaseModel):
    """landing page table"""
    PREFIX = 'LP-'

    class Status(IntegerChoices):
        UNPUBLISHED = 0
        PUBLISHED = 1
        SUSPEND = 2
        DELETE = 3

        # STATUS_CHOICES = [(UNPUBLISHED, '未发布'), (PUBLISHED, '投放中'), (SUSPEND, '停止'), (DELETE, '删除')]

    STATUS_ENUM = [Status.UNPUBLISHED, Status.PUBLISHED, Status.SUSPEND, Status.DELETE]

    name = CharField(verbose_name="投放页名称", max_length=32, default='')
    unique_id = CharField(verbose_name='唯一标识符', null=False, blank=False, max_length=32)
    url = CharField(verbose_name='超链接', max_length=255, default='')
    status = IntegerField(
        verbose_name="发布状态: UNPUBLISHED = 0 PUBLISHED = 1 SUSPEND = 2 DELETE = 3 "
                     "[(UNPUBLISHED, 未发布), (PUBLISHED, 投放中), (SUSPEND, 停止), (DELETE, 删除)]",
        choices=Status.choices, default=Status.UNPUBLISHED)
    company = VirtualForeignKey(Company, on_delete=CASCADE, related_name='company_landing_pages')
    account = VirtualForeignKey(AgentAccount, on_delete=CASCADE, related_name='account_landing_pages')

    objects = MyManager()
    all_objects = MyAllManager()

    class Meta:
        db_table = AGENT_PREFIX + 'landing_page'

    @classmethod
    def create(cls, **kwargs):
        unique_id = generate_uuid(cls.PREFIX)
        kwargs.update({'unique_id': unique_id})
        obj = super().create(**kwargs)
        return obj
