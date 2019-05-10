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

class DepartmentChangeStatus(object):
    UNEXECUTED = "unexecuted"
    EXECUTED = "executed"
    CHOICES = ((UNEXECUTED, '未执行'), (EXECUTED, "已执行"))


class DepartmentChange(BaseModel):

    staff = ForeignKey(Staff, related_name = "change_staff", on_delete=CASCADE)
    adder = ForeignKey(Staff, related_name = "change_adder", null = True, on_delete=CASCADE)
    executor = ForeignKey(Staff, related_name = "change_executor", null = True, on_delete=CASCADE)

    department_front = ForeignKey(Department, related_name = "change_department_front", null = True, on_delete=CASCADE)
    department_now = ForeignKey(Department, related_name = "change_department_now", null = True, on_delete=CASCADE)

    start_time = DateTimeField(verbose_name = "开始时间", null = True, blank = True)
    end_time = DateTimeField(verbose_name = "结束时间", null = True, blank = True)

    remark = TextField(verbose_name = "备注", default = "")
    status = CharField(verbose_name = "状态", max_length = 32, choices = DepartmentChangeStatus.CHOICES, default = DepartmentChangeStatus.UNEXECUTED)
    update_time = DateTimeField(verbose_name = "更新时间", auto_now = True)
    create_time = DateTimeField(verbose_name = "创建时间", default = timezone.now)

    @classmethod
    def search(cls, **attrs):
        department_qs = cls.query().filter(**attrs)
        return department_qs
