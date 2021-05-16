# -*- coding: UTF-8 -*-    
# Author: Dongjd
# FileName: model_landingpagevent
# DateTime: 2020/12/7 17:36
# Project: operate_backend_be
# Do Not Touch Me!


from django.db.models import *

from model import AGENT_PREFIX
from model.fields import VirtualForeignKey
from model.store.model_event_base import AEventBase
from model.store.model_forms import Form
from model.store.model_landingpage import LandingPage


class FormEvent(AEventBase):
    class ActionTypes(IntegerChoices):
        CREATE = 0
        DELETE = 1
        EDIT = 2

        # CHOICES = [(CREATE, "创建"), (DELETE, "删除")]

    form = VirtualForeignKey(Form, on_delete=CASCADE)
    action = IntegerField(verbose_name="操作类型: CREATE = 0 DELETE = 1"
                                       "[(CREATE, 创建), (DELETE, 删除),", default=ActionTypes.CREATE,
                          choices=ActionTypes.choices)

    class Meta:
        db_table = AGENT_PREFIX + 'form_event'


class LandingPageEvent(AEventBase):
    class ActionTypes(IntegerChoices):
        CREATE = 0
        DELETE = 1
        PUBLISH = 2
        SUSPEND = 3
        RENAME = 4
        COPY = 5

        # CHOICES = [(CREATE, '创建'), (DELETE, '删除'), (PUBLISH, '发布'), (SUSPEND, '停止')]

    landing_page = VirtualForeignKey(LandingPage, on_delete=CASCADE)
    action = IntegerField(
        verbose_name="操作类型: CREATE = 0 DELETE = 1 PUBLISH = 2 SUSPEND = 3 "
                     "[(CREATE, 创建), (DELETE, 删除),"
                     " (PUBLISH, 发布), (SUSPEND, 停止)], (RENAME, 重命名), (COPY, 创建副本)",
        default=ActionTypes.CREATE, choices=ActionTypes.choices)

    class Meta:
        db_table = AGENT_PREFIX + 'landing_page_event'
