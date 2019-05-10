# coding=UTF-8

'''
Created on 2016年7月22日

@author: Administrator
'''

from django.db.models import *
from model.base import BaseModel
from model.store.model_user import Staff
from model.store.model_department import Department


class MeasureStaff(BaseModel):
    """员工绩效"""
    staff = ForeignKey(Staff, related_name="measure_staff", null=True, on_delete=CASCADE)
    record = ForeignKey(Staff, related_name="measure_record", null=True, on_delete=CASCADE)
    department = ForeignKey(Department, null=True, on_delete=CASCADE)

    new_number = IntegerField(verbose_name="当日新分数据", default=0)
    exhale_number = IntegerField(verbose_name="当日呼出数", default=0)
    call_number = IntegerField(verbose_name="当日接通数", default=0)
    wechat_number = IntegerField(verbose_name="添加微信数", default=0)
    report_date = DateField(verbose_name="报表日期", max_length=20, null=True, blank=True)

    remark = TextField(verbose_name="备注")

    update_time = DateTimeField(verbose_name="更新时间", auto_now=True)
    create_time = DateTimeField(verbose_name="创建时间", auto_now_add=True)

    @classmethod
    def search(cls, **attrs):
        measure_staff_qs = cls.query().filter(**attrs)
        return measure_staff_qs

    @classmethod
    def get_annotate_data(cls, measure_staff_qs):
        iter_obj = measure_staff_qs.values_list('staff', 'department').annotate(Sum('new_number'), Sum('exhale_number'),
                                                                                Sum('call_number'),
                                                                                Sum('wechat_number'))
        return iter_obj
