# -*- coding: utf-8 -*-
# file_name       : members.py
# file_func       :
# file_author     : 'Johnathan.Wick'
# file_create_date: 2019/9/28 16:38
import datetime

from django.db import models
from django.utils import timezone
from BuyGoods.models_store import BaseModel


class BaseMembers(BaseModel):
    IDENTITY = (
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
    username = models.CharField(max_length=64, default='Anonymous', null=False)
    password = models.CharField(max_length=128, default='123456', null=False)
    user_rank = models.IntegerField(default=3, choices=IDENTITY)
    user_type = models.IntegerField(default=2, choices=U_Type)
    brief = models.TextField(default='the guy is too laze , nothing left behind')
    address = models.CharField(max_length=512, default='Mars')

    class Meta:
        abstract = True


class Token(models.Model):
    identity = models.CharField(max_length=128, null=False)
    token = models.CharField(max_length=128, null=False)
    create_time = models.DateTimeField(default=timezone.now)

    @property
    def datetime_expired(self, days=30):
        s_time = timezone.now()
        e_time = datetime.timedelta(days=days) + self.create_time
        return True if s_time < e_time else False


class Users(BaseMembers):
    GENDER = (
        (0, 'female'),
        (1, 'male'),
        (2, 'freak'),
        (3, 'unsure')
    )
    gender = models.IntegerField(default=3, choices=GENDER)
    rank = models.IntegerField(verbose_name='user rank', default=0)

    class Meta:
        db_table = 'buy_users'


class Merchants(BaseMembers):
    class Meta:
        db_table = 'buy_merchants'


class Managers(BaseMembers):
    class Meta:
        db_table = 'buy_managers'
