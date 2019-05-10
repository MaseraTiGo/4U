# coding=UTF-8

from tuoen.sys.log.base import logger
from model.store.model_user import Staff
from support.generator.base import BaseGenerator


class StaffGenerator(BaseGenerator):

    def __init__(self, staff_info):
        super(StaffGenerator, self).__init__()
        self._staff_infos = self.init(staff_info)

    def get_create_list(self, result_mapping):
        return self._staff_infos

    def create(self, staff_info, result_mapping):
        staff_qs = Staff.query().filter(identity = staff_info.identity)
        if staff_qs.count():
            staff = staff_qs[0]
        else:
            staff = Staff.create(**staff_info)
        return staff

    def delete(self):
        print('======================>>> delete staff <======================')
        return None
