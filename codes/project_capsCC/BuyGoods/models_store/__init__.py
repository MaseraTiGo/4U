# -*- coding: utf-8 -*-
# file_name       : __init__.py.py
# file_func       :
# file_author     : 'Johnathan.Wick'
# file_create_date: 2019/9/27 15:22

from django.db import models
from django.utils import timezone


class BaseModel(models.Model):
    update_time = models.DateTimeField(auto_now=True)
    create_time = models.DateTimeField(default=timezone.now)
    remark = models.TextField(verbose_name='details', null=True, default='')

    class Meta:
        abstract = True
