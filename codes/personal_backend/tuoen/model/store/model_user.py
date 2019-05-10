# coding=UTF-8

'''
Created on 2016年7月22日

@author: Administrator
'''

from django.db.models import *
from django.utils import timezone
from model.base import BaseModel
from model.store.model_shop import Shop


class GenderTypes(object):
    MAN = "man"
    WOMAN = "woman"
    UNKNOWN = "unknown"
    CHOICES = ((MAN, '男士'), (WOMAN, "女士"), (UNKNOWN, "未知"))


class BaseUser(BaseModel):
    """用户基础验证表"""
    identity = CharField(verbose_name="身份证号", max_length=24, default="", null=True)
    name = CharField(verbose_name="姓名", max_length=64, default="")
    gender = CharField(verbose_name="性别", max_length=24, choices=GenderTypes.CHOICES, default=GenderTypes.UNKNOWN)
    birthday = DateField(verbose_name="生日", null=True, blank=True)

    phone = CharField(verbose_name="手机号", max_length=20, default="", null=True)
    email = CharField(verbose_name="邮箱", max_length=128, default="", null=True)

    city = CharField(verbose_name="城市", max_length=128, default="", null=True)
    address = TextField(verbose_name="详细地址", default="", null=True)
    remark = TextField(verbose_name="备注", default="", null=True)

    update_time = DateTimeField(verbose_name="更新时间", auto_now=True)
    create_time = DateTimeField(verbose_name="创建时间", default=timezone.now)

    class Meta:
        abstract = True

    @classmethod
    def get_userinfo_buyid(cls, id):
        """ 根据id查询个人信息 """
        try:
            return cls.objects.filter(id=id)[0]
        except:
            return None


class EducationType(object):
    PRIMARY = "primary"
    MIDDLE = "middle"
    HIGH = "high"
    UNDERGRADUAYE = "undergraduate"
    COLLEGE = "college"
    MIDDLECOLLEGE = "middlecollege"
    MASTER = "master"
    DOCTOR = "doctor"
    OTHER = "other"
    CHOICES = ((PRIMARY, '小学'), (MIDDLE, "初中"), (HIGH, "高中"), (UNDERGRADUAYE, "本科"), (COLLEGE, "大专"), \
               (MIDDLECOLLEGE, "中专"), (MASTER, "硕士"), (DOCTOR, "博士"), (OTHER, "其他"))


class Staff(BaseUser):
    """员工表"""
    number = CharField(verbose_name="员工工号", max_length=128)
    emergency_contact = CharField(verbose_name="紧急联系人", max_length=64, default="")
    emergency_phone = CharField(verbose_name="紧急联系人电话", max_length=20, default="")
    entry_time = DateField(verbose_name="入职时间", null=True, blank=True)
    education = CharField(verbose_name="学历", max_length=24, choices=EducationType.CHOICES, default=EducationType.OTHER)
    bank_number = CharField(verbose_name="招行卡号", max_length=32, default="")
    bank_name = CharField(verbose_name="招行卡号", max_length=32, default="")
    contract_b = CharField(verbose_name="合同编号（必）", max_length=64, default="")
    contract_l = CharField(verbose_name="合同编号（立）", max_length=64, default="")
    expire_time = DateField(verbose_name="到期时间", null=True, blank=True)
    quit_time = DateField(verbose_name="离职时间", null=True, blank=True)
    is_working = BooleanField(verbose_name="是否在职", default=True)
    is_admin = BooleanField(verbose_name="是否是管理员", default=False)
    p_start_time = DateTimeField(verbose_name="保护开始时间", null=True, blank=True)
    p_end_time = DateTimeField(verbose_name="保护截止时间", null=True, blank=True)

    @classmethod
    def get_staff_byname(cls, name):
        """根据姓名查询员工"""
        try:
            return cls.query().filter(name=name)[0]
        except:
            return None

    @classmethod
    def search(cls, **attrs):
        staff_qs = cls.query().filter(**attrs)
        return staff_qs

    @classmethod
    def create(cls, **kwargs):
        staff = super().create(**kwargs)
        if staff is not None:
            number = "BQ{number}".format(number=(staff.id + 10000))
            staff.update(number=number)

        return staff
