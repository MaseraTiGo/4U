# coding=UTF-8

'''
Created on 2016年7月22日

@author: Administrator
'''

from django.db.models import *

from model.base import BaseModel
from model.fields import VirtualForeignKey
from model.store.model_account import AgentAccount


class AEventBase(BaseModel):
    """事件基类表"""
    account = VirtualForeignKey(AgentAccount, on_delete=CASCADE, related_name='staff_%(class)s')

    remark = CharField(verbose_name="备注", default="", max_length=250)

    class Meta:
        abstract = True
