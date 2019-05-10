# coding=UTF-8
'''
created on 20180608
@author: djd
'''

from tuoen.abs.middleware.role import role_middleware
from tuoen.abs.middleware.department import department_middleware

from model.store.model_user import Staff
from model.store.model_auth_access import AuthAccess
from model.store.model_role import Role


class UserRightServer(object):
    """用户权限控制"""
    _staff_qs = None
    _is_admin = False
    _staff_id_list = []
    _is_show_sub = True
    _cur_user_id = 0
    _is_show_all = False

    def __init__(self, cur_user):
        self._cur_user_id = cur_user.id
        role_access = AuthAccess.search(staff=cur_user, access_type='role')
        try:
            role_id = role_access[0].access_id
            self._is_show_all = any(r.is_show_all for r in Role.search(id=role_id))
        except IndexError as _:
            pass
        if cur_user.is_admin or self._is_show_all:
            self._is_admin = True
            self._staff_qs = Staff.query()
            self._staff_id_list = [s.id for s in self._staff_qs]
        else:
            all_sub_ids = []
            all_sub__department_ids = []
            role_id_list = [ac.access_id for ac in AuthAccess.query().filter(staff=cur_user,
                                                                             access_type='role')]
            dept_id_list = [ac.access_id for ac in AuthAccess.query().filter(staff=cur_user, access_type='department')]
            for role_id in role_id_list:
                sub_list = role_middleware.get_all_children_ids(role_id)
                self._is_show_sub = Role.query().filter(id=role_id)[0].is_show_data
                if self._is_show_sub:
                    all_sub_ids.extend(sub_list)
            role_id_list = [acs.staff_id for acs in
                            AuthAccess.query().filter(access_id__in=all_sub_ids, access_type='role')
                            ]
            for dept_id in dept_id_list:
                all_sub__department_ids.append(dept_id)
                dept_list = department_middleware.get_all_children_ids(dept_id)
                all_sub__department_ids.extend(dept_list)

            dept_id_list = [acs.staff_id for acs in \
                            AuthAccess.query().filter(access_id__in=all_sub__department_ids, access_type='department')
                            ]
            staff_id_list = list(set(role_id_list).intersection(set(dept_id_list)))
            staff_id_list.append(cur_user.id)
            self._staff_id_list = staff_id_list
            self._staff_qs = Staff.query().filter(id__in=staff_id_list)
