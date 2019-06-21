# -*- coding: utf-8 -*-
# file_func  :
# file_author: 'Johnathan.Wick'
# file_date  : '6/12/2019 11:29 AM'

from django.db import models
from django.utils import timezone
from ..models.basemodel import CapsCBaseModel


class Labels(models.Model):
    CHOICE = ((),)

    region = models.CharField(max_length=33, default='NoWhere')
    shape = models.CharField(max_length=50, default='Unknown')
    age = models.CharField(max_length=50, default='Young')


class BeautyBase(models.Model):
    pass


class Beauty(models.Model):
    REGION = (
        ('Asia', '亚洲'),
        ('European', '欧洲'),
        ('USA', '美洲')
    )
    SKIN_CHOICE = (
        ('Yellow', '黄色'),
        ('LightYellow', '浅黄'),
        ('White', '白皙'),
        ('LightBlack', '浅黑')
    )
    BRA_SIZE = (
        ('A', 'A罩杯'),
        ('B', 'B罩杯'),
        ('B+', 'B+罩杯'),
        ('C', 'C罩杯'),
        ('C+', 'C+罩杯'),
        ('D', 'D罩杯'),
        ('D+', 'D+罩杯'),
        ('E', 'E罩杯'),
        ('H', 'H罩杯'),
        ('G', 'G罩杯'),
        ('G++', 'G++罩杯')
    )
    name = models.CharField(max_length=33, default='LittleBoot')
    skin = models.CharField(max_length=13, default='Yellow', choices=SKIN_CHOICE)
    age = models.IntegerField(default=0)
    region = models.CharField(max_length=33, default='Asia', choices=REGION)
    country = models.CharField(max_length=66, default='Japan')
    height = models.CharField(max_length=3, default='0')
    shape = models.CharField(max_length=50, default='Unknown')
    bra = models.CharField(max_length=6, default='B')
    img = models.ImageField(upload_to='avatar')
    create_time = models.DateTimeField(default=timezone.now)
    update_time = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'Beauty'

    @classmethod
    def search(cls, **kwargs):
        cls_qs = cls.objects.filter(**kwargs)
        return cls_qs
