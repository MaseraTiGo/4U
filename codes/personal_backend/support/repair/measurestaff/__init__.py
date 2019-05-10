# coding=UTF-8

import json

from model.store.model_measure_staff import MeasureStaff
from model.store.model_auth_access import AuthAccess, AccessTypes
from model.store.model_department import Department


class MeasureStaffRepair():


    def run(self):
        self.ready()

        i = 0
        measure_staff_qs = MeasureStaff.search()
        print("==========员工绩效数：", len(measure_staff_qs))

        for measure_staff in measure_staff_qs:
            i = i + 1
            if i % 1000 == 0:
                print("=========>>>>>>>处理:", i)

            if measure_staff.staff in self._all_auth_access:
                auth_access = self._all_auth_access[measure_staff.staff]
                department = self._all_department[auth_access.access_id]
                measure_staff.update(department = department)


    def ready(self):
        self._all_auth_access = {}
        self._all_department = {}
        auth_access_qs = AuthAccess.search(access_type = AccessTypes.DEPARTMENT)
        print("=====员工部门关系数据数=====", len(auth_access_qs))
        for auth_access in auth_access_qs:
            if auth_access.staff not in self._all_auth_access:
                self._all_auth_access[auth_access.staff] = auth_access

        department_qs = Department.search()
        print("=====部门数据数=====", len(department_qs))
        for department in department_qs:
            self._all_department[department.id] = department

        print("=====数据准备完成=====")

