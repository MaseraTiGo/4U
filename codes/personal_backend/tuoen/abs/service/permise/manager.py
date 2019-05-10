# coding=UTF-8

'''
Created on 2016年7月22日

@author: Administrator
'''

import hashlib
import datetime
import json
import random

from tuoen.sys.core.exception.business_error import BusinessError
from tuoen.sys.utils.common.split_page import Splitor

from model.models import AuthAccess, AccessTypes

from tuoen.abs.middleware.role import role_middleware
from tuoen.abs.middleware.department import department_middleware
# from tuoen.abs.middleware.rule import rule_middleware

from tuoen.abs.service.permise.staff.department import DepartmentHelper
from tuoen.abs.service.permise.staff.role import RoleHelper
from tuoen.abs.service.permise.staff.department import DepartmentChangeHelper


class StaffPermiseServer(object):

    @classmethod
    def generate_staff_access(cls, access_ids, access_type, staff):
        """创建员工权限关系"""

        if access_type == "role":
            for access_id in access_ids:
                cls.generate(access_id, access_type, staff)
        elif access_type == "department":
            for access_id in access_ids:
                cls.generate(access_id, access_type, staff)

    @classmethod
    def search_qs(cls, **search_info):
        """查询员工权限关系"""
        auth_access_qs = AuthAccess.search(**search_info)
        return auth_access_qs

    @classmethod
    def search_staffids_bydepartmentid(cls, department_id):
        department_ids = department_middleware.get_all_children_ids(department_id)
        department_ids.append(department_id)
        staff_ids = [a.staff_id for a in cls.search_qs(access_id__in = department_ids, \
                                                            access_type = AccessTypes.DEPARTMENT)]
        return staff_ids

    @classmethod
    def get_staff_department(cls, staff):
        """获取员工部门"""
        auth_access_qs = cls.search_qs(staff = staff, access_type = AccessTypes.DEPARTMENT)
        department = None
        if auth_access_qs.count() > 0:
            department = department_middleware.get_self(auth_access_qs[0].access_id)
        else:
            raise BusinessError("该员工没有部门")

        return department

    @classmethod
    def get_staff_department_ids(cls, staff):
        """获取员工部门以及下级部门id"""
        auth_access_qs = cls.search_qs(staff = staff, access_type = AccessTypes.DEPARTMENT)
        department_ids = []
        for auth_access in auth_access_qs:
            department_ids.append(auth_access.access_id)
            dept_list = department_middleware.get_all_children_ids(auth_access.access_id)
            department_ids.extend(dept_list)

        return list(set(department_ids))

    @classmethod
    def update_staff_access(cls, access_ids, access_type, staff):
        """修改员工权限关系"""

        cls.remove(staff, access_type)
        for access_id in access_ids:
            cls.generate(access_id, access_type, staff)

    @classmethod
    def generate(cls, access_id, access_type, staff, is_main='no'):
        """添加员工权限关系"""

        auth_access = AuthAccess.create(access_id = access_id, access_type = access_type, staff = staff, is_main=is_main)
        '''
        if auth_access is None:
            raise BusinessError("关系绑定失败")

        return auth_access
        '''

    @classmethod
    def remove(self, staff, access_type):
        """解除员工下的所有关系"""
        delete_qs = AuthAccess.query(access_type = access_type, staff = staff, is_main='no')
        delete_qs.delete()

    @classmethod
    def unbundling(cls, id):
        """删除员工关系绑定"""

        auth_access = AuthAccess.get_byid(id)
        if auth_access is None:
            raise BusinessError("此关系不存在")

        auth_access.delete()
        return True

    @classmethod
    def is_exit(cls, access_id, access_type, staff_id):
        """此权限关系是否存在"""

        auth_access_qs = AuthAccess.query(access_id = access_id, access_type = access_type, \
                                          staff_id = staff_id)
        if auth_access_qs.count() > 0:
            return True
        return False

    @classmethod
    def modify(cls, id, access_id):
        """修改员工绑定的角色或部门"""

        auth_access = AuthAccess.get_byid(id)
        if auth_access is None:
            raise BusinessError("此关系不存在")

        auth_access.update(access_id = access_id)
        return True

    @classmethod
    def get_rules_bystaff(cls, staff):
        """通过员工获得所有的功能"""

        rulestr = ""
        auth_access_list = AuthAccess.query(staff = staff, access_type = AccessTypes.ROLE)
        rule_list = []
        for authaccess in auth_access_list:
            role = RoleServer.get(authaccess.access_id)
            rule_list.extend(role.rule_list)
        return rule_list

    @classmethod
    def hung_permise_bystaff(cls, staff):
        """员工对象挂载权限"""
        authaccess_list = AuthAccess.query(staff = staff)
        department_ids = []
        role_ids = []
        for access in authaccess_list:
            if access.access_type == "department":
                department_ids.append(access.access_id)
            else:
                role_ids.append(access.access_id)
        staff.role_list = role_middleware.get_list_byids(role_ids)
        staff.department_list = department_middleware.get_list_byids(department_ids)
        return staff

    @classmethod
    def hung_permise_forstaffs(cls, staff_list):
        """员工列表挂载权限"""

        authaccess_list = AuthAccess.query(staff__in = staff_list)

        # 循环关系表求出角色id集合和部门id集合
        staff_mapping = {}
        department_id_list = []
        role_id_list = []
        for access in authaccess_list:
            staff = access.staff

            if staff.id not in staff_mapping:
                staff_mapping[staff.id] = {
                    'role_list': [],
                    'department_list': []
                }
            if access.access_type == "department":
                if access.is_main != 'yes':
                    staff_mapping[staff.id]['department_list'].append(access.access_id)
                    department_id_list.append(access.access_id)
            else:
                staff_mapping[staff.id]['role_list'].append(access.access_id)
                role_id_list.append(access.access_id)

        department_mapping = { department.id: department \
                    for department in department_middleware.get_list_byids(department_id_list)}

        role_mapping = { role.id: role for role in role_middleware.get_list_byids(role_id_list)}

        for staff in staff_list:
            staff_info = staff_mapping.get(staff.id)
            if staff_info is None:
                staff.department_list = []
                staff.role_list = []
            else:
                staff.department_list = [department_mapping[dep_id] \
                                         for dep_id in staff_info['department_list'] \
                                            if dep_id in department_mapping]
                staff.role_list = [role_mapping[role_id] \
                                    for role_id in staff_info['role_list'] \
                                        if role_id in role_mapping]

        return staff_list

    @classmethod
    def get_all_children(cls, staff):
        """查询所有同部门的下级的角色"""
        authaccess_list = AuthAccess.query(staff = staff)
        department_ids = []
        role_ids = []
        for access in authaccess_list:
            if access.access_type == "role":
                role_ids.extend(role_middleware.get_all_children_ids(access.access_id))
            else:
                department_ids.append(access.access_id)

        role_ids = list(set(role_ids))
        return role_ids, department_ids

    @classmethod
    def get_children(cls, staff):
        """查询同部门下一级角色"""
        authaccess_list = AuthAccess.query(staff = staff)
        department_ids = []
        role_ids = []
        for access in authaccess_list:
            if access.access_type == "role":
                role_ids.extend(role_middleware.get_children_ids(access.access_id))
            else:
                department_ids.append(access.access_id)

        role_ids = list(set(role_ids))
        return role_ids, department_ids

    @classmethod
    def get_staffs_byauthaccess(cls, **attrs):
        staff_list = []
        authaccess_list = AuthAccess.search(**attrs)
        for authaccess in authaccess_list:
            staff_list.append(authaccess.staff)
        return  staff_list

    @classmethod
    def get_all_children_staff(cls, staff):
        """查询同部门所有下级员工"""
        role_ids = []
        department_ids = []
        role_ids, department_ids = cls.get_all_children(staff)
        children_staff_role = cls.get_staffs_byauthaccess(access_type = AccessTypes.ROLE, access_id__in = role_ids)
        children_staff_department = cls.get_staffs_byauthaccess(access_type = AccessTypes.DEPARTMENT, access_id__in = department_ids)
        children_staff_list = list(set(children_staff_role) & set(children_staff_department))

        return children_staff_list

    @classmethod
    def get_all_children_staff(cls, staff):
        """查询同部门下一级员工"""
        role_ids = []
        department_ids = []
        role_ids, department_ids = cls.get_children(staff)
        children_staff_role = cls.get_staffs_byauthaccess(access_type = AccessTypes.ROLE, access_id__in = role_ids)
        children_staff_department = cls.get_staffs_byauthaccess(access_type = AccessTypes.DEPARTMENT, access_id__in = department_ids)
        children_staff_list = list(set(children_staff_role) & set(children_staff_department))

        return children_staff_list

    @classmethod
    def get_myall_level(cls, staff):
        """查询自己统计和所有的下级角色和部门"""
        role_list = []
        department_list = []
        own_roleids = []
        own_departmentids = []
        auth_access_list = AuthAccess.query(staff = staff)
        for auth_access in auth_access_list:
            if auth_access.access_type == AccessTypes.ROLE:
                own_roleids.append(auth_access.access_id)
                role_list.extend(role_middleware.get_all_children(auth_access.access_id))
            if auth_access.access_type == AccessTypes.DEPARTMENT:
                own_departmentids.append(auth_access.access_id)
                department_list.extend(department_middleware.get_all_children(auth_access.access_id))

        role_list.extend(RoleServer.search(id__in = own_roleids))
        department_list.extend(DepartmentServer.search(id__in = own_departmentids))

        return list(set(role_list)), list(set(department_list))


class RoleServer(object):

    @classmethod
    def add(cls, **role_info):
        return RoleHelper.generate(**role_info)

    @classmethod
    def search(cls, **attrs):
        return RoleHelper.search(**attrs)

    @classmethod
    def update(cls, role, **attrs):
        return RoleHelper.update(role, **attrs)

    @classmethod
    def remove(cls, role_id):
        return RoleHelper.remove(role_id)

    @classmethod
    def get(cls, role_id):
        return RoleHelper.get(role_id)

    @classmethod
    def is_exit(cls, role_id):
        return RoleHelper.is_exit(role_id)

    @classmethod
    def is_name_exist(cls, name, role = None):
        return RoleHelper.is_name_exist(name, role)

class DepartmentServer(object):

    @classmethod
    def add(cls, **department_info):
        return DepartmentHelper.generate(**department_info)

    @classmethod
    def search(cls, **attrs):
        return DepartmentHelper.search(**attrs)

    @classmethod
    def update(cls, department, **attrs):
        return DepartmentHelper.update(department, **attrs)

    @classmethod
    def remove(cls, department_id):
        return DepartmentHelper.remove(department_id)

    @classmethod
    def get(cls, department_id):
        return DepartmentHelper.get(department_id)

    @classmethod
    def is_exit(cls, department_id):
        return DepartmentHelper.is_exit(department_id)

    @classmethod
    def is_name_exist(cls, name, department = None):
        return DepartmentHelper.is_name_exist(name, department)


class DepartmentChangeServer(object):

    @classmethod
    def generate(cls, **department_change_info):
        """创建部门调岗任务"""
        return DepartmentChangeHelper.generate(**department_change_info)

    @classmethod
    def search(cls, current_page, **search_info):
        """查询部门调岗任务列表"""
        return DepartmentChangeHelper.search(current_page, **search_info)

    @classmethod
    def get(cls, department_change_id):
        """获取部门调岗任务详情"""
        return DepartmentChangeHelper.get(department_change_id)

    @classmethod
    def update(cls, department_change, **attrs):
        """编辑部门调岗任务"""
        return DepartmentChangeHelper.update(department_change, **attrs)

    @classmethod
    def remove(cls, department_change):
        """删除部门调岗任务"""
        return DepartmentChangeHelper.remove(department_change)

    @classmethod
    def executed(cls, department_change, auth_user):
        """执行部门调岗任务"""
        return DepartmentChangeHelper.executed(department_change, auth_user)
