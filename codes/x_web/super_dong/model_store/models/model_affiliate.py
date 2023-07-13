# -*- coding: utf-8 -*-
# @File    : model_affiliate
# @Project : x_web
# @Time    : 2023/7/11 14:33
# once, I want 2 leave my name 2 the history
# sadly, I find that my hair gets pale
"""                     
                                      /             
 __.  , , , _  _   __ ______  _    __/  __ ____  _, 
(_/|_(_(_/_</_/_)_(_)/ / / <_</_  (_/_ (_)/ / <_(_)_
                                                 /| 
                                                |/  
"""
from django.db.models import URLField, CharField, IntegerField, ForeignKey, \
    SET_NULL, IntegerChoices, DecimalField, SmallIntegerField, JSONField, \
    DateTimeField, ManyToManyField

from const import fucking_prefix
from super_dong.frame.utils import gen_unique_id_by_str
from super_dong.model_store.base import BaseModel, BaseAccount, Status
from super_dong.model_store.models.model_account import Tool
from super_dong.model_store.models.model_data_set import WhitePig

prefix = 'affiliate'


class Affiliate(BaseModel):
    name = CharField(verbose_name='affiliate name', max_length=32, unique=True)
    url = URLField(verbose_name='url')
    unique_id = IntegerField(verbose_name='unique id')

    @classmethod
    def create(cls, **kwargs):
        if 'unique_id' not in kwargs:
            kwargs.update(
                {
                    "unique_id": gen_unique_id_by_str(kwargs['name']) // 1000
                }
            )
        print(f"{fucking_prefix} {kwargs['unique_id']}")
        return super().create(**kwargs)

    class Meta:
        db_table = f"{prefix}_networking"


class AffiliateAccount(BaseAccount):
    affiliate = ForeignKey(Affiliate, on_delete=SET_NULL, null=True)

    class Meta:
        db_table = f"{prefix}_account"


class Offer(BaseModel):
    class Category(IntegerChoices):
        UNDEFINED = 0, 'UNDEFINED'
        SALE = 1, 'SALE'
        EDU = 2, 'EDU'

    class Currency(IntegerChoices):
        US = 0, 'US'
        CN = 1, 'CN'
        UK = 2, 'UK'
        AU = 3, 'AU'
        JP = 4, 'JP'

    affiliate_account = ForeignKey(AffiliateAccount, on_delete=SET_NULL, null=True)

    category = IntegerField(
        verbose_name='category',
        default=Category.UNDEFINED,
        choices=Category.choices
    )
    price = DecimalField(verbose_name='price', max_digits=13, decimal_places=2)
    currency = SmallIntegerField(
        verbose_name='currency',
        default=Currency.US,
        choices=Currency.choices
    )
    cur_conversion = IntegerField(verbose_name='cur conversion')
    max_conversion_limit = IntegerField(
        verbose_name='max_conversion_limit'
    )
    active_region = JSONField(verbose_name='active_region', default=list)
    status = SmallIntegerField(
        verbose_name='status',
        default=Status.ACTIVE,
        choices=Status.choices
    )
    end_datetime = DateTimeField(verbose_name='datetime')

    class Meta:
        db_table = f'{prefix}_offer'


class Run(BaseModel):
    offer = ForeignKey(Offer, on_delete=SET_NULL, null=True)
    pig = ForeignKey(WhitePig, on_delete=SET_NULL, null=True)

    tools = ManyToManyField(
        Tool,
        symmetrical=False,
        related_name='all_runs'
    )

    status = IntegerField(
        verbose_name='run status',
        default=Status.UNCONVERTED,
        choices=Status.choices,
    )

    class Meta:
        db_table = f'{prefix}_run'
