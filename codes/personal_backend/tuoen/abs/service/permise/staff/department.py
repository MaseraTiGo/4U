# coding=UTF-8

'''
Created on 2016年7月22日

@author: Administrator
'''

import hashlib
import datetime
import json
import random

from django.db.models import *

from tuoen.sys.core.exception.business_error import BusinessError
from tuoen.sys.utils.common.split_page import Splitor

from tuoen.abs.middleware.department import department_middleware

from model.models import Department, AuthAccess
from model.store.model_department_change import DepartmentChange, DepartmentChangeStatus
from model.store.model_order_event import StaffOrderEvent
from model.store.model_measure_staff import MeasureStaff



class DepartmentHelper(object):

    @classmethod
    def generate(cls, **department_info):
        """创建部门"""

        department = Department.create(**department_info)
        if department is None:
            raise BusinessError("部门创建失败")

        department_middleware.force_refresh()
        return department

    @classmethod
    def search(cls, **attrs):
        """查询部门列表"""
        department_list = Department.search(**attrs)
        return department_list

    @classmethod
    def get(cls, department_id):
        """获取部门详情"""
        department = Department.get_byid(department_id)
        if department is None:
            raise BusinessError("该部门不存在")
        return department

    @classmethod
    def update(cls, department, **attrs):
        """编辑部门"""
        department.update(**attrs)
        department_middleware.force_refresh()

        return True

    @classmethod
    def remove(cls, department_id):
        """删除部门"""

        access_type = "department"
        auth_access = AuthAccess.get_by_access_id(department_id, access_type)
        if auth_access.count() > 0:
            raise BusinessError("已绑定用户无法删除")

        department_children = department_middleware.get_children(department_id)
        if department_children:
            raise BusinessError("此部门存在下级无法删除")

        department = Department.get_byid(department_id)
        if department is None:
            raise BusinessError("该部门不存在")

        department.delete()

        department_middleware.force_refresh()

        return True

    @classmethod
    def is_exit(cls, department_id):
        """判断该角色是否存在"""
        department = Department.get_byid(department_id)
        if department is None:
            return False
        return True

    @classmethod
    def is_name_exist(cls, name, department = None):
        """判断部门名称是否存在"""
        department_qs = Department.search(name = name)

        if department is not None:
            department_qs = department_qs.filter(~Q(id = department.id))

        if department_qs.count() > 0:
            raise BusinessError("该名称已存在")
        return True

class DepartmentChangeHelper(object):

    @classmethod
    def generate(cls, **department_change_info):
        """创建部门调岗任务"""

        department_change = DepartmentChange.create(**department_change_info)
        if department_change is None:
            raise BusinessError("部门调岗任务创建失败")

        return department_change

    @classmethod
    def search(cls, current_page, **search_info):
        """查询部门调岗任务列表"""

        keyword = ""
        if "keyword" in search_info:
            keyword = search_info.pop("keyword")

        department_change_qs = DepartmentChange.search(**search_info)

        if keyword:
            department_change_qs = department_change_qs.filter(Q(staff__name__contains = keyword) \
                        | Q(staff__number__contains = keyword))

        department_change_qs = department_change_qs.order_by("-create_time")
        return Splitor(current_page, department_change_qs)


    @classmethod
    def get(cls, department_change_id):
        """获取部门调岗任务详情"""
        department_change = DepartmentChange.get_byid(department_change_id)
        if department_change is None:
            raise BusinessError("该部门调岗任务不存在")
        return department_change

    @classmethod
    def update(cls, department_change, **attrs):
        """编辑部门调岗任务"""
        department_change.update(**attrs)

        return True

    @classmethod
    def remove(cls, department_change):
        """删除部门调岗任务"""
        department_change.delete()

        return True

    @classmethod
    def executed(self, department_change, auth_user):
        """执行部门调岗任务"""
        if department_change.status == DepartmentChangeStatus.EXECUTED:
            raise BusinessError("请不要重复执行该调岗任务")

        search_info_orderevent = {}
        search_info_measurestaff = {}
        update_info = {}

        search_info_orderevent.update({"staff":department_change.staff})
        search_info_measurestaff.update({"staff":department_change.staff})
        if department_change.department_front:
            search_info_orderevent.update({"department":department_change.department_front})
            search_info_measurestaff.update({"department":department_change.department_front})

        search_info_orderevent.update({"order__pay_time__lte":department_change.end_time})
        search_info_measurestaff.update({"report_date__lte":department_change.end_time})

        if department_change.start_time:
            search_info_orderevent.update({"order__pay_time__gte":department_change.start_time})
            search_info_measurestaff.update({"report_date__gte":department_change.start_time})

        update_info.update({"department":department_change.department_now})

        StaffOrderEvent.search(**search_info_orderevent).update(**update_info)
        MeasureStaff.search(**search_info_measurestaff).update(**update_info)

        department_change.update(status = DepartmentChangeStatus.EXECUTED, executor = auth_user)




