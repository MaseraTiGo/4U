# coding=UTF-8

import random
from tuoen.sys.utils.common.dictwrapper import DictWrapper
from tuoen.sys.log.base import logger
from model.store.model_auth_access import AccessTypes, AuthAccess
from support.generator.base import BaseGenerator
from support.generator.helper.role import RoleGenerator
from support.generator.helper.department import DepartmentGenerator
from support.generator.helper.staff import StaffGenerator


class AuthAccessGenerator(BaseGenerator):

    def get_create_list(self, result_mapping):
        staff_list = result_mapping.get(StaffGenerator.get_key())
        role_list = result_mapping.get(RoleGenerator.get_key())
        department_list = result_mapping.get(DepartmentGenerator.get_key())

        auth_list = []
        for staff in staff_list:
            if staff.id == 1:
                department = department_list[0]
                role = role_list[0]
            else:
                department = random.choice(department_list)
                role = random.choice(role_list)
                
            auth_access_department = DictWrapper({})
            auth_access_department.staff = staff
            auth_access_department.access_id = department.id
            auth_access_department.access_type = AccessTypes.DEPARTMENT

            auth_access_role = DictWrapper({})
            auth_access_role.staff = staff
            auth_access_role.access_id = role.id
            auth_access_role.access_type = AccessTypes.ROLE

            auth_list.append(auth_access_department)
            auth_list.append(auth_access_role)

        return auth_list

    def create(self, access, result_mapping):
        auth_access_qs = AuthAccess.query().filter(**access)
        if auth_access_qs.count():
            auth_access = auth_access_qs[0]
        else:
            auth_access = AuthAccess.create(**access)
        return auth_access

    def delete(self):
        print('======================>>> delete auth_access <======================')
        return None
