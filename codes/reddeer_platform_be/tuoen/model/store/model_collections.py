# -*- coding: UTF-8 -*-    
# Author: Dongjd
# FileName: model_collections
# DateTime: 2020/12/7 17:12
# Project: operate_backend_be
# Do Not Touch Me!


from django.db.models import *

from model import AGENT_PREFIX
from model.base import BaseModel
from model.fields import VirtualForeignKey
from model.store.model_customer import Customer
from model.store.model_forms import Form
from model.store.model_landingpage import LandingPage


class Collections(BaseModel):
    """collections table"""

    customer = VirtualForeignKey(Customer, on_delete=CASCADE, related_name='customer_collections', null=True)
    # landing_page = VirtualForeignKey(LandingPage, on_delete=CASCADE,
    #                                  related_name='landing_page_collections', null=True)
    # form = VirtualForeignKey(Form, on_delete=CASCADE, related_name='form_collections', null=True)
    detail_data = JSONField(verbose_name="提交信息详情", default=dict)
    is_valid = BooleanField(verbose_name='数据有效性', default=True)
    remark = CharField(verbose_name="备注", default='', max_length=64)

    class Meta:
        db_table = AGENT_PREFIX + 'collection'
