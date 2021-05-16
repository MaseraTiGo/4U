# coding=UTF-8

'''
Created on 2016年7月22日

@author: Administrator
'''

import datetime

from django.db.models import *

from model.base import BaseModel


def default_date():
    return datetime.date(1900, 1, 1)


class BaseUser(BaseModel):
    """用户基础验证表"""
    MAN = "man"
    WOMAN = "woman"
    UNKNOWN = "unknown"
    GENDER_CHOICES = ((MAN, '男士'), (WOMAN, "女士"), (UNKNOWN, "未知"))

    identity = CharField(verbose_name="身份证号", max_length=18, default="")
    name = CharField(verbose_name="姓名", max_length=32, default="")
    gender = CharField(verbose_name="性别", max_length=8, choices=GENDER_CHOICES, default=UNKNOWN)
    birthday = DateField(verbose_name="生日", default=default_date)

    phone = CharField(verbose_name="手机号", max_length=16, default="")
    email = CharField(verbose_name="邮箱", max_length=64, default="")

    city = CharField(verbose_name="城市", max_length=32, default="")
    address = CharField(verbose_name="详细地址", default="", max_length=64)
    remark = CharField(verbose_name="备注", default="", max_length=64)

    class Meta:
        abstract = True

    @classmethod
    def get_userinfo_buyid(cls, id):
        """ 根据id查询个人信息 """
        try:
            return cls.objects.filter(id=id)[0]
        except:
            return None


class Staff(BaseUser):
    """员工表"""
    number = CharField(verbose_name="员工工号", max_length=8)
    is_admin = BooleanField(verbose_name="是否是管理员", default=False)

    class Meta:
        # db_table = 'staff'
        abstract = True

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
            number = "RD{number}".format(number=(staff.id + 10000))
            staff.update(number=number)

        return staff
