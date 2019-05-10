# coding=UTF-8

'''
Created on 2016年7月22日

@author: Administrator
'''

from django.db.models import *
from django.utils import timezone
from model.base import BaseModel
from model.store.model_user import Staff
from model.store.model_department import Department


class MobileDeviceStatus(object):
     NORMAL = "normal"
     SCRAP = "scrap"
     IDLE = "idle"
     OTHER = "other"
     CHOICES = ((NORMAL, '正常'), (SCRAP, "报废"), (IDLE, "闲置"), (OTHER, "其它"))

class MobileDevices(BaseModel):
    code = CharField(verbose_name = "手机设备编码", max_length = 64, default = "")
    brand = CharField(verbose_name = "手机品牌", max_length = 64, default = "")
    model = CharField(verbose_name = "手机型号", max_length = 64, default = "")
    price = IntegerField(verbose_name = "购买价格/分", default = 0)
    status = CharField(verbose_name = "手机设备状态", max_length = 32, choices = MobileDeviceStatus.CHOICES, default = MobileDeviceStatus.NORMAL)
    remark = TextField(verbose_name = "备注", default = "")
    imei = CharField(verbose_name = "手机imei号", max_length = 128, default = "")

    update_time = DateTimeField(verbose_name = "更新时间", auto_now = True)
    create_time = DateTimeField(verbose_name = "创建时间", default = timezone.now)

    @classmethod
    def search(cls, **attrs):
        mobile_devices_qs = cls.query().filter(**attrs)
        return mobile_devices_qs

class MobileStatus(object):
     NORMAL = "normal"
     FROZEN = "frozen"
     SEAL = "seal"
     ARREARS = "arrears"
     DISCONTINUATION = "discontinuation"
     OTHER = "other"
     CHOICES = ((NORMAL, '正常'), (FROZEN, "冻结"), (SEAL, "封号"), (ARREARS, "欠费"), (DISCONTINUATION, "停用"), (OTHER, "其它"))


class Mobilephone(BaseModel):
    devices = ForeignKey(MobileDevices, null = True, on_delete=CASCADE)

    staff = ForeignKey(Staff, null = True, on_delete=CASCADE)
    leader = CharField(verbose_name = "负责人", max_length = 64, default = "")
    t_member = CharField(verbose_name = "组员", max_length = 64, default = "")
    name = CharField(verbose_name = "姓名", max_length = 64, default = "")
    identity = CharField(verbose_name = "身份证", max_length = 64, default = "")
    phone_number = CharField(verbose_name = "手机号", max_length = 64, default = "")
    flow_card_number = CharField(verbose_name = "流量卡号", max_length = 128, default = "")
    card_password = CharField(verbose_name = "手机卡密码", max_length = 64, default = "")
    department = ForeignKey(Department, null = True, on_delete=CASCADE)
    operator = CharField(verbose_name = "运营商", max_length = 64, default = "")
    rent = IntegerField(verbose_name = "月租/分", default = 0)

    tag = CharField(verbose_name = "标签", max_length = 128, default = "")
    phone_remark = TextField(verbose_name = "手机号备注", default = "")
    phone_change = TextField(verbose_name = "手机号变更信息", default = "")
    status = CharField(verbose_name = "手机号状态", max_length = 32, choices = MobileStatus.CHOICES, default = MobileStatus.NORMAL)

    wechat_nick = CharField(verbose_name = "微信昵称", max_length = 128, default = "")
    wechat_number = CharField(verbose_name = "微信号", max_length = 128, default = "")
    wechat_password = CharField(verbose_name = "微信密码", max_length = 64, default = "")
    wechat_remark = TextField(verbose_name = "微信备注", default = "")
    pay_password = CharField(verbose_name = "支付密码", max_length = 64, default = "")

    update_time = DateTimeField(verbose_name = "更新时间", auto_now = True)
    create_time = DateTimeField(verbose_name = "创建时间", default = timezone.now)

    @classmethod
    def search(cls, **attrs):
        mobile_maintain_qs = cls.query().filter(**attrs)
        return mobile_maintain_qs

class MobileMaintain(BaseModel):
    devices = ForeignKey(MobileDevices, on_delete=CASCADE)
    staff = ForeignKey(Staff, on_delete=CASCADE)
    remark = TextField(verbose_name = "备注", default = "")

    update_time = DateTimeField(verbose_name = "更新时间", auto_now = True)
    create_time = DateTimeField(verbose_name = "创建时间", default = timezone.now)

    @classmethod
    def search(cls, **attrs):
        mobile_maintain_qs = cls.query().filter(**attrs)
        return mobile_maintain_qs
