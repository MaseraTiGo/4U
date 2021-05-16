# coding=UTF-8

'''
Created on 2016年7月22日

@author: Administrator
'''

from django.db.models import *

from model import AGENT_PREFIX
from model.base import BaseModel
from model.fields import VirtualForeignKey
from model.store.model_forms import Form
from model.store.model_landingpage import LandingPage


class LandingPageComponent(BaseModel):
    """component table"""

    class CType(IntegerChoices):
        PIC = 0
        BTN = 1
        SLID = 2
        FORM = 3
        DOCS = 4

        # COMPONENT_TYPE_CHOICES = [(PIC, '图片'), (BTN, '按钮'), (SLID, '轮播'), (FORM, '表单')]

    landing_page = VirtualForeignKey(LandingPage, on_delete=CASCADE,
                                     related_name='landing_page_components')
    index = IntegerField(verbose_name="序位", default=0)
    name = CharField(verbose_name="组件名称", max_length=32, default='')
    c_type = IntegerField(verbose_name="组件类型: PIC = 0 BTN = 1 SLID = 2 FORM = 3 "
                                       "[(PIC, 图片), (BTN, 按钮), (SLID, 轮播), (FORM, 表单)]",
                          default=CType.PIC,
                          choices=CType.choices)
    attrs = JSONField(verbose_name='组件属性', default=dict)

    class Meta:
        db_table = AGENT_PREFIX + 'landing_page_component'


class FormComponent(BaseModel):
    """component table"""

    class CType(IntegerChoices):
        TEXT = 1
        RADIO = 2
        ADDRESS = 3
        CHECKBOX = 4
        PICS = 5
        DIY = 6
        DOCS = 7
        ATTACH = 8

    class Tag(IntegerChoices):
        NAME = 0
        PHONE = 1
        AGE = 2
        GENDER = 3
        TEXT = 4
        POSITION = 5
        ADDR = 6
        JOB = 7
        DEPARTMENT = 8
        COMPANY = 9
        WEB = 10
        TEL = 11
        FAX = 12
        PICS = 13
        DIY = 14
        DOCS = 15
        ATTACH = 16

    form = VirtualForeignKey(Form, on_delete=CASCADE, related_name='form_components')
    name = CharField(verbose_name="组件名称", max_length=32, default='')
    describe = CharField(verbose_name='描述', max_length=32, default='')
    is_needed = BooleanField(verbose_name='是否必填', default=True)
    index = IntegerField(verbose_name="序位", default=0)
    tag = IntegerField(verbose_name='标识: NAME = 0 PHONE = 1 AGE = 2 GENDER = 3 TEXT = 4 RADIO = 5 '
                                    'ADDRESS = 6 CHECKBOX = 7 ATTACH = 16'
                                    '[(NAME, 姓名), (PHONE, 手机), (AGE, 年龄), (GENDER, 性别), '
                                    '(TEXT, 文本), (RADIO, 单选), (ADDRESS, 地址), (CHECKBOX, 多选), (ATTACH, 附件)]',
                       default=Tag.NAME, choices=Tag.choices)
    c_type = IntegerField(verbose_name='组件类型: [(TEXT, 文本, 1), (RADIO, 单选, 2), (ADDRESS, 地址, 3), (CHECKBOX, 多选, 4)'
                                       '(ATTACH, 附件, 8)]',
                          default=CType.TEXT, choices=CType.choices)
    attrs = JSONField(verbose_name='组件属性', default=dict)

    class Meta:
        db_table = AGENT_PREFIX + 'form_component'
