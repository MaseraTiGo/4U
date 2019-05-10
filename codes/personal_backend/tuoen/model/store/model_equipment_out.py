# coding=UTF-8

'''
Created on 2016年7月22日

@author: Administrator
'''

from django.db.models import *
from django.utils import timezone
from model.base import BaseModel


class AgentTypes(object):
    SELF = "self"
    FIRST = "first"
    SECOND = "second"
    CHOICES = ((SELF, '自营平台'), (FIRST, "一级代理"), (SECOND, "二级代理"))


class EquipmentOut(BaseModel):
    """SN设备出库信息"""

    add_time = DateField(verbose_name = "添加时间", max_length = 20, null = True, blank = True)
    agent_name = CharField(verbose_name = "代理商名称", max_length = 32, default = "")
    agent_phone = CharField(verbose_name = "代理商电话", max_length = 32, null = True, default = "")
    product_type = CharField(verbose_name = "产品类型", max_length = 32, default = "")
    product_model = CharField(verbose_name = "产品型号", max_length = 32, default = "")
    min_number = BigIntegerField (verbose_name = "起始号段")
    max_number = BigIntegerField (verbose_name = "终止号段")
    quantity = IntegerField(verbose_name = "入库数量", default = 0)
    price = CharField(verbose_name = "单价", max_length = 32, null = True, default = "")
    salesman = CharField(verbose_name = "业务员", max_length = 32, null = True, default = "")
    address = CharField(verbose_name = "发货地址", max_length = 128, null = True, default = "")
    rate = CharField(verbose_name = "签约费率", max_length = 32, null = True, default = "")
    remark = TextField(verbose_name = "出货备注", max_length = 128, default = "")
    type = CharField(verbose_name = "出库类型", max_length = 24, choices = AgentTypes.CHOICES, default = AgentTypes.SELF)

    create_time = DateTimeField(verbose_name = "创建时间", default = timezone.now)
    update_time = DateTimeField(verbose_name = "更新时间", auto_now = True)

    @classmethod
    def search(cls, **attrs):
        equipment_out_qs = cls.query().filter(**attrs)
        return equipment_out_qs
