# -*- coding: utf-8 -*-
# file_name       : members.py
# file_func       :
# file_author     : 'Johnathan.Wick'
# file_create_date: 2019/9/28 16:38

from django.db import models
from BuyGoods.models_store import BaseModel


class BaseMembers(BaseModel):
    RANK = (
        (0, 'admin'),
        (1, 'svip'),
        (2, 'vip'),
        (3, 'poor'),
    )
    U_Type = (
        (0, 'Platform'),
        (1, 'Merchant'),
        (2, 'User')
    )
    username = models.CharField(max_length=64, default='Anonymous', null=True)
    password = models.CharField(max_length=16, default='123456', null=True)
    user_rank = models.IntegerField(default=3, choices=RANK)
    user_type = models.IntegerField(default=2, choices=U_Type)

    class Meta:
        abstract = True


class Users(BaseMembers):
    class Meta:
        db_table = 'buy_users'


class Merchants(BaseMembers):
    class Meta:
        db_table = 'buy_merchants'


class Managers(BaseMembers):
    class Meta:
        db_table = 'buy_managers'
