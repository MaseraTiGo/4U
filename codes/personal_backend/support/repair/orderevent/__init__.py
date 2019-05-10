# coding=UTF-8

import json

from model.store.model_order_event import StaffOrderEvent
from model.store.model_auth_access import AuthAccess, AccessTypes
from model.store.model_department import Department


class OrderEventRepair():
    # 先清理重复

    def run(self):
        self.ready()

        i = 0
        staff_order_event_qs = StaffOrderEvent.search()
        print("==========订单事件数：", len(staff_order_event_qs))

        for order_event in staff_order_event_qs:
            i = i + 1
            if i % 1000 == 0:
                print("=========>>>>>>>处理:", i)

            if order_event.staff in self._all_auth_access:
                auth_access = self._all_auth_access[order_event.staff]
                department = self._all_department[auth_access.access_id]
                order_event.update(department = department)


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

