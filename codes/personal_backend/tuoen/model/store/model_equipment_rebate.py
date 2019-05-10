# coding=UTF-8

'''
Created on 2016年7月22日

@author: Administrator
'''

from django.db.models import *
from django.utils import timezone
from model.base import BaseModel
from model.store.model_equipment_register import EquipmentRegister


class EquipmentRebate(BaseModel):
    """返利表"""
    agent_id = CharField(verbose_name = "代理商ID", max_length = 64, default = "", null = True)
    agent_name = CharField(verbose_name = "代理商名称", max_length = 32, default = "", null = True)
    code = ForeignKey(EquipmentRegister, null = True, on_delete=CASCADE)
    name = CharField(verbose_name = "客户名称", max_length = 64, default = "", null = True)
    phone = CharField(verbose_name = "注册手机号", max_length = 32, default = "", null = True)
    activity_type = CharField(verbose_name = "活动类型", max_length = 32, null = True)
    register_code = CharField(verbose_name = "客户编码", max_length = 32)

    register_time = DateField(verbose_name = "注册时间", null = True, blank = True)
    bind_time = DateField(verbose_name = "绑定时间", null = True, blank = True)
    month = DateField(verbose_name = "交易月份", null = True, blank = True)
    transaction_amount = IntegerField(verbose_name = "交易金额/分", default = 0)
    effective_amount = IntegerField(verbose_name = "有效金额/分", default = 0)
    accumulate_amount = IntegerField(verbose_name = "当月累计交易金额/分", default = 0)
    history_amount = IntegerField(verbose_name = "历史累计交易金额/分", default = 0)
    type = CharField(verbose_name = "号段类型", max_length = 32, null = True)
    is_rebate = CharField(verbose_name = "是否返利", max_length = 32, default = "", null = True)
    remark = TextField(verbose_name = "备注", null = True)

    update_time = DateTimeField(verbose_name = "更新时间", auto_now = True)
    create_time = DateTimeField(verbose_name = "创建时间", default = timezone.now)

    @classmethod
    def search(cls, **attrs):
        equipment_register_qs = cls.query().filter(**attrs)
        return equipment_register_qs
