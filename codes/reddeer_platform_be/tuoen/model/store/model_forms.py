# coding=UTF-8

'''
Created on 2016年7月22日

@author: Administrator
'''

from django.db.models import *

from model import AGENT_PREFIX
from model.base import BaseModel
from model.fields import VirtualForeignKey, VirtualManyToManyField
from model.store.model_company import Company
from model.store.model_landingpage import LandingPage
from model.store.utils import generate_uuid


class Form(BaseModel):
    """form table"""
    PREFIX = 'FM-'

    name = CharField(verbose_name='表单名称', max_length=32, default='')
    is_limited = BooleanField(verbose_name='限填一次', default=False)
    is_title_hide = BooleanField(verbose_name='是否隐藏表头', default=True)
    unique_id = CharField(verbose_name='唯一标识符', null=False, blank=False, max_length=32)
    company = VirtualForeignKey(Company, on_delete=CASCADE, related_name='company_forms')
    # landing_page = VirtualForeignKey(LandingPage, on_delete=SET_DEFAULT, default='',
    # related_name='landing_page_forms')
    # landing_pages = VirtualManyToManyField(LandingPage, related_name='landing_page_forms')
    is_delete = BooleanField(verbose_name='删除标记', default=False)
    url = CharField(verbose_name='链接', max_length=255, default='')

    class Meta:
        db_table = AGENT_PREFIX + 'form'

    @classmethod
    def create(cls, **kwargs):
        unique_id = generate_uuid(cls.PREFIX)
        kwargs.update({'unique_id': unique_id})
        obj = super().create(**kwargs)
        return obj
