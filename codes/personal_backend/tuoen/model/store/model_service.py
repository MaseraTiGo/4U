# coding=UTF-8

'''
Created on 2016年7月22日

@author: Administrator
'''

from django.db.models import *
from django.utils import timezone
from model.base import BaseModel
from model.store.model_user import Staff
from model.store.model_equipment import Equipment, EquipmentStatusType
from model.store.model_equipment_sn import EquipmentSn
from model.store.model_customer import Customer
from model.store.model_order import Order


class Service(BaseModel):
    """售后服务表"""
    seller = ForeignKey(Staff, related_name = "service_seller", null = True, on_delete=CASCADE)
    server = ForeignKey(Staff, related_name = "service_server", null = True, on_delete=CASCADE)
    customer = ForeignKey(Customer, on_delete=CASCADE)
    order = ForeignKey(Order, null = True, on_delete=CASCADE)
    end_time = DateTimeField(verbose_name = "截止时间", max_length = 20, null = True, blank = True)

    remark = TextField(verbose_name = "备注")

    update_time = DateTimeField(verbose_name = "更新时间", auto_now = True)
    create_time = DateTimeField(verbose_name = "创建时间", default = timezone.now)

    @classmethod
    def search(cls, **attrs):
        service_qs = cls.query().filter(**attrs)
        return service_qs


class ServiceItem(BaseModel):
    """售后服务单产品详情"""
    customer = ForeignKey(Customer, null = True, on_delete=CASCADE)
    service = ForeignKey(Service, null = True, on_delete=CASCADE)
    equipment = ForeignKey(Equipment, null = True, on_delete=CASCADE)
    equipment_sn = ForeignKey(EquipmentSn, null = True, on_delete=CASCADE)
    order = ForeignKey(Order, null = True, db_index = True, on_delete=CASCADE)

    buyinfo_status = CharField(verbose_name = "购买信息状态", max_length = 64, choices = EquipmentStatusType.CHOICES, default = EquipmentStatusType.RED)
    dsinfo_status = CharField(verbose_name = "点刷信息状态", max_length = 64, choices = EquipmentStatusType.CHOICES, default = EquipmentStatusType.RED)
    rebate_status = CharField(verbose_name = "激活信息状态", max_length = 64, choices = EquipmentStatusType.CHOICES, default = EquipmentStatusType.RED)
    sn_status = CharField(verbose_name = "设备码出入库状态", max_length = 64, choices = EquipmentStatusType.CHOICES, default = EquipmentStatusType.RED)

    remark = TextField(verbose_name = "备注", default = "")

    update_time = DateTimeField(verbose_name = "更新时间", auto_now = True)
    create_time = DateTimeField(verbose_name = "创建时间", default = timezone.now)


    @classmethod
    def search(cls, **attrs):
        service_item_qs = cls.query().filter(**attrs)
        return service_item_qs
