# coding=UTF-8

from django.db.models import *
from django.utils import timezone
from model.base import BaseModel


class Config(BaseModel):
    type_desc = CharField(verbose_name="类别描述", max_length=16)
    type = CharField(verbose_name="类别", max_length=16)
    name = CharField(verbose_name="名称", max_length=16)
    key = CharField(verbose_name="key", max_length=16)
    value = CharField(verbose_name="value", max_length=32, default="")

    class Meta:
        db_table = 'config'
