# coding=UTF-8

'''
Created on 2016年7月22日

@author: Administrator
'''

from django.db.models import *
from django.utils import timezone
from model.base import BaseModel
from model.store.model_equipment import Equipment
from model.store.model_equipment_sn import EquipmentSn


class SourceTypes(object):
    YSB = "ysb"
    OTHER = "other"
    CHOICES = ((YSB, '银收宝'), (OTHER, "其它"))


class Merchant(BaseModel):
    """商户表"""
    merchant_id = CharField(verbose_name = "商户编号", max_length = 128, default = "")
    merchant_name = CharField(verbose_name = "商户名称", max_length = 64, default = "")
    organ_id = CharField(verbose_name = "机构编号（代理商编号）", max_length = 64, default = "")
    organ_name = CharField(verbose_name = "机构名称", max_length = 64, default = "")
    organ_level = CharField(verbose_name = "机构等级", max_length = 64, default = "")
    real_name = CharField(verbose_name = "真实姓名", max_length = 32, default = "")
    id_card = CharField(verbose_name = "身份证号 ", max_length = 32, default = "")
    phone = CharField(verbose_name = "手机号", max_length = 64, default = "", null = True)
    reg_date = DateTimeField(verbose_name = "注册时间", null = True, blank = True)
    pid = CharField(verbose_name = "产品编号 ", max_length = 32, default = "")

    source = CharField(verbose_name = "商户来源", max_length = 32, choices = SourceTypes.CHOICES, default = SourceTypes.OTHER)
    is_activation = IntegerField(verbose_name = "是否激活 ", default = 0)

    update_time = DateTimeField(verbose_name = "更新时间", auto_now = True)
    create_time = DateTimeField(verbose_name = "创建时间", default = timezone.now)

    @classmethod
    def search(cls, **attrs):
        merchant_qs = cls.query().filter(**attrs)
        return merchant_qs
