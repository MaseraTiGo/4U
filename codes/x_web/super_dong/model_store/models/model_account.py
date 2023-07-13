# -*- coding: utf-8 -*-
# @File    : model_account
# @Project : x_web
# @Time    : 2023/7/11 15:18
# once, I want 2 leave my name 2 the history
# sadly, I find that my hair gets pale
"""                     
                                      /             
 __.  , , , _  _   __ ______  _    __/  __ ____  _, 
(_/|_(_(_/_</_/_)_(_)/ / / <_</_  (_/_ (_)/ / <_(_)_
                                                 /| 
                                                |/  
"""
from django.db.models import CharField, IntegerField, IntegerChoices, \
    ForeignKey, SET_NULL, DecimalField, DateTimeField, IPAddressField

from super_dong.model_store.base import BaseModel, BaseAccount

prefix = 'tool'


class Tool(BaseModel):
    class Category(IntegerChoices):
        UNDEFINED = 0, 'UNDEFINED'
        PROXY = 1, 'PROXY'
        SIMULATE = 2, 'SIMULATE'

    name = CharField(verbose_name='name', max_length=32)
    category = IntegerField(
        verbose_name='category',
        choices=Category.choices,
        default=Category.PROXY
    )
    price = DecimalField(verbose_name='price', max_digits=13, decimal_places=2)

    class Meta:
        db_table = f'{prefix}_set'


class ToolAccount(BaseAccount):
    tool = ForeignKey(Tool, on_delete=SET_NULL, null=True)

    class Meta:
        db_table = f'{prefix}_account'


class ToolPay(BaseModel):
    pay_amount = DecimalField(verbose_name='pay amount', max_digits=13, decimal_places=2)
    expire_at = DateTimeField(verbose_name='expire datetime')

    class Meta:
        db_table = f'{prefix}_pay'


class ProxyUsing(BaseModel):
    ...
