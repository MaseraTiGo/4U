# coding=UTF-8

'''
Created on 2016年7月22日

@author: Administrator
'''

import hashlib
import datetime
import json
import random

from django.db.models import Q

from tuoen.sys.core.exception.business_error import BusinessError
from tuoen.sys.utils.common.split_page import Splitor
from tuoen.abs.service.user.token import Token
from tuoen.abs.middleware.role import role_middleware
from tuoen.abs.middleware.department import department_middleware
from tuoen.abs.middleware.role import role_middleware

from model.models import Staff
from model.models import AuthAccess, AccessTypes
from model.models import Role
from model.models import Department
from model.store.model_order_event import StaffOrderEvent, IsCount
from model.store.model_measure_staff import MeasureStaff
from model.store.model_department_change import DepartmentChange, DepartmentChangeStatus


class UserServer(object):

    @classmethod
    def generate_token(cls, user):
        return Token.generate(user.id, user.__class__.__name__)

    @classmethod
    def renew_token(cls, auth_str, renew_str):
        token = Token.get(auth_str)
        token.renew(renew_str)
        return token

    @classmethod
    def get_token(cls, auth_str, parms=None):
        token = Token.get(auth_str)
        token.check(parms)
        return token


class StaffServer(object):

    @classmethod
    def register(cls, **attrs):
        """添加员工"""
        staff = Staff.create(**attrs)
        if staff is None:
            raise BusinessError("员工添加失败")
        if 'p_start_time' in attrs:
            cls.add_work_time(staff.id, **attrs)
        return staff

    @classmethod
    def get(cls, staff_id):
        """获取员工个人信息"""
        staff = Staff.get_byid(staff_id)
        if staff is None:
            raise BusinessError("员工不存在")
        return staff

    @classmethod
    def get_staff_security(cls, staff):
        is_security = False
        auth_access_qs = AuthAccess.search(staff=staff, access_type=AccessTypes.ROLE)
        for auth_access in auth_access_qs:
            role = role_middleware.get_self(auth_access.access_id)
            if role.is_security:
                is_security = True
        staff.is_security = is_security
        return staff

    @classmethod
    def update(cls, staff, **attrs):
        """修改员工个人信息"""
        staff.update(**attrs)
        return staff

    @classmethod
    def search(cls, current_page, **search_info):
        """查询员工列表"""

        if 'cur_user' in search_info:
            user_pro = search_info.pop('cur_user')
            staff_qs = user_pro._staff_qs
        else:
            staff_qs = Staff.query()

        if 'keyword' in search_info:
            keyword = search_info.pop('keyword')
            staff_qs = staff_qs.filter(Q(name__contains=keyword) | \
                                       Q(phone__contains=keyword))
        dept_staff_id = []
        role_staff_id = []
        d_flag = False
        r_flag = False
        if 'department' in search_info:
            d_flag = True
            dept_id = search_info.pop('department')
            # dept_id = [d.id for d in Department.query().filter(name__contains = dept)] #使用名称查找
            department_ids = department_middleware.get_all_children_ids(dept_id)
            department_ids.append(dept_id)
            dept_staff_id = [a.staff_id for a in
                             AuthAccess.query().filter(access_id__in=department_ids, access_type='department')]
        if 'role' in search_info:
            r_flag = True
            role_id = search_info.pop('role')
            # role_id = [r.id for r in Role.query().filter(name__contains = role)] #使用名称查找
            role_staff_id = [a.staff_id for a in
                             AuthAccess.query().filter(access_id__exact=role_id, access_type='role')]
        if all((d_flag, r_flag)):
            staff_id_list = list(set(role_staff_id).intersection(set(dept_staff_id)))
            staff_qs = staff_qs.filter(id__in=staff_id_list)
        elif not d_flag and not r_flag:
            pass
        else:
            staff_id_list = dept_staff_id + role_staff_id
            staff_qs = staff_qs.filter(id__in=staff_id_list)
        if 'is_working' in search_info:
            is_working = search_info.pop('is_working')
            staff_qs = staff_qs.filter(is_working=is_working)
        staff_qs = staff_qs.order_by("-entry_time")
        temp = []
        for staff in staff_qs:
            try:
                aa_obj = AuthAccess.search(staff=staff, access_type='department', is_main='yes')[0]
                staff.main_dept = aa_obj.access_id
            except IndexError as _:
                staff.main_dept = 1
            try:
                staff.main_dept_name = Department.search(id=staff.main_dept)[0].name
            except IndexError as _:
                staff.main_dept_name = 'unknown'
            temp.append(staff)
        staff_qs = temp
        return Splitor(current_page, staff_qs)

    @classmethod
    def search_all(cls, **search_info):
        """查询所有员工列表"""
        staff_qs = Staff.search(**search_info)
        staff_qs = staff_qs.order_by("-create_time")

        return staff_qs

    @classmethod
    def match(cls, keyword, size=5):
        """查询员工列表"""
        return Staff.query(name=keyword).order_by('-create_time')[:size]

    @classmethod
    def get_staff_byname(cls, name):
        """根据姓名查询员工"""
        staff = Staff.get_staff_byname(name=name)
        return staff

    @classmethod
    def is_name_exist(cls, name):
        """判断员工姓名是否存在"""

        staff = cls.get_staff_byname(name=name)

        if staff is not None:
            raise BusinessError("该名称已存在")
        return True

    @classmethod
    def check_exist(cls, identity, staff=None):
        """判断身份证号是否存在"""

        staff_identity_qs = Staff.query(identity=identity)
        if staff is not None:
            staff_identity_qs = staff_identity_qs.filter(~Q(id=staff.id))
        if staff_identity_qs.count() > 0:
            raise BusinessError("该身份证号已存在")

        return True

    @classmethod
    def judge_staff_role(cls, admin):
        """判断员工是否为管理员"""
        if not admin.is_admin:
            raise BusinessError("当前身份不为管理员")
        return True

    @classmethod
    def user_info(cls, user):
        try:
            aa_qs = AuthAccess.query(staff=user)
            dept_qs = aa_qs.filter(access_type='department')
            dept_name = [Department.query(id=dept.access_id)[0].name for dept in dept_qs]
            role_qs = aa_qs.filter(access_type='role')
            role_name = [Role.query(id=role.access_id)[0].name for role in role_qs]
            user.department = '-'.join(dept_name)
            user.role = '-'.join(role_name)
        except Exception as e:
            pass
        return user

    @classmethod
    def add_work_time(cls, staff_id, **input_info):
        staff_obj = Staff.search(id=staff_id)[0]
        staff_obj.p_start_time = input_info['p_start_time']
        if 'p_end_time' in input_info:
            staff_obj.p_end_time = input_info['p_end_time']
        else:
            input_info['p_end_time'] = ''
        staff_obj.save()
        if input_info['p_end_time'] != '':
            update_info = {'order__pay_time__gte': input_info['p_start_time'],
                           'order__pay_time__lte': input_info['p_end_time'],
                           'staff': staff_obj}
            StaffOrderEvent.search(**update_info).update(**{'is_count': IsCount.COUNTOUT})
        return True

    @classmethod
    def transfer_position(cls, staff_id, **input_info):
        search_info = {'staff_id': staff_id, 'access_type': 'department', 'is_main': 'yes'}
        try:
            aa_obj = AuthAccess.search(**search_info)[0]
        except IndexError as _:
            # raise BusinessError("员工数据异常")
            aa_obj = AuthAccess.search(**{'staff_id': staff_id, 'access_type': 'department'})[0]
        aa_obj.access_id = input_info['desc_dept']
        aa_obj.save()
        transfer_time = input_info['transfer_time']
        desc_dept = input_info['desc_dept']
        staff_obj = Staff.search(id=staff_id)[0]
        src_dept_obj = Department.search(id=input_info['src_dept'])[0]
        desc_dept_obj = Department.search(id=input_info['desc_dept'])[0]
        record_info = {'staff': staff_obj, 'adder': input_info['operator'],
                       'department_front': src_dept_obj, 'department_now': desc_dept_obj,
                       'status': DepartmentChangeStatus.EXECUTED}
        DepartmentChange.create(**record_info)
        cls.fix_data_cause_by_transfer(staff_id, transfer_time, desc_dept)
        return True

    @classmethod
    def fix_data_cause_by_transfer(cls, staff_id, transfer_time, desc_dept):
        cls.fix_measure_staff(staff_id, transfer_time, desc_dept)
        cls.fix_order_event(staff_id, transfer_time, desc_dept)
        return True

    @classmethod
    def fix_measure_staff(cls, staff_id, transfer_time, desc_dept):
        search_info = {'staff_id': staff_id, 'report_date__gte': transfer_time}
        ms_qs = MeasureStaff.search(**search_info)
        ms_qs.update(**{'department_id': desc_dept})
        return True

    @classmethod
    def fix_order_event(cls, staff_id, transfer_time, desc_dept):
        search_info = {'staff_id': staff_id, 'order__pay_time__gte': transfer_time}
        soe_qs = StaffOrderEvent.search(**search_info)
        soe_qs.update(**{'department_id': desc_dept})
        return True
