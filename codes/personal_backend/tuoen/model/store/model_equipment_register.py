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


class RegisterTypes(object):
    NORMAL = "normal"
    ABNORMAL = "abnormal"
    AGENT = "agent"
    CHOICES = ((NORMAL, '正常'), (ABNORMAL, "异常"), (AGENT, "代理商"))

class EquipmentRegister(BaseModel):
    """设备注册表"""
    equipment = ForeignKey(Equipment, null = True, on_delete=CASCADE)
    equipment_sn = ForeignKey(EquipmentSn, null = True, on_delete=CASCADE)
    agent_name = CharField(verbose_name = "代理商名称", max_length = 64, default = "")
    code = CharField(verbose_name = "客户编码", max_length = 32, default = "")
    phone = CharField(verbose_name = "注册手机号", max_length = 32, default = "")
    name = CharField(verbose_name = "客户姓名", max_length = 64, default = "", null = True)
    register_time = DateTimeField(verbose_name = "创建时间", default = timezone.now)
    bind_time = DateTimeField(verbose_name = "绑定时间", default = timezone.now)
    device_code = CharField(verbose_name = "设备编码", max_length = 32, default = "")
    status = CharField(verbose_name = "状态", max_length = 32, choices = RegisterTypes.CHOICES, default = RegisterTypes.NORMAL)

    update_time = DateTimeField(verbose_name = "更新时间", auto_now = True)
    create_time = DateTimeField(verbose_name = "创建时间", default = timezone.now)

    @classmethod
    def search(cls, **attrs):
        equipment_register_qs = cls.query().filter(**attrs)
        return equipment_register_qs
