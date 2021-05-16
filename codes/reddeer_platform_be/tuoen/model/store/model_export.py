# coding=UTF-8

from django.db.models import *
from django.utils import timezone
from model.base import BaseModel


class Export(BaseModel):
    name = CharField(verbose_name="下载名称", max_length=128, default="")
    type = CharField(verbose_name="下载类别", max_length=64, default="")
    url = TextField(verbose_name="下载连接", default="")

    class Meta:
        abstract = True

    @classmethod
    def search(cls, **kwargs):
        export_qs = cls.query().filter(**kwargs)
        return export_qs
