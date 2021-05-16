# coding=UTF-8

from django.db.models import *
from django.utils import timezone
from model.base import BaseModel


class SourceTypes(object):
    BIND_SN = 'bind_sn'
    CHOICES = ((BIND_SN, '绑定sn'),)


class StatusTypes(object):
    SUCCESS = 'success'
    FAIL = 'fail'
    RESEND = 'resend'
    CHOICES = ((SUCCESS, '成功'), (FAIL, "失败"), (RESEND, "已重发"))


class Sms(BaseModel):
    phone = CharField(verbose_name="手机号", max_length=32)
    template_id = CharField(verbose_name="模板id", max_length=64)
    template_label = CharField(verbose_name="模板标签", max_length=64)
    param = TextField(verbose_name="参数")
    content = TextField(verbose_name="内容")
    label = CharField(verbose_name="短信平台标签", max_length=64, default='haoservice_sms')
    unique_no = CharField(verbose_name="唯一标识", max_length=128, default='')
    scene = CharField(verbose_name="场景标识", max_length=64, choices=SourceTypes.CHOICES, default=SourceTypes.BIND_SN)
    source_type = CharField(verbose_name="接收短信的用户来源平台", max_length=64, default='')
    status = CharField(verbose_name="发送状态", max_length=32, choices=StatusTypes.CHOICES, default=StatusTypes.SUCCESS)

    class Meta:
        # 4 now , wo do not need it. so we won't create this model.
        abstract = True

    @classmethod
    def search(cls, **attrs):
        sms_qs = cls.query().filter(**attrs)
        return sms_qs
