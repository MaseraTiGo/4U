# coding=UTF-8

import json
from tuoen.sys.utils.common.dictwrapper import DictWrapper
from tuoen.sys.log.base import logger
from model.store.model_equipment import Equipment
from support.generator.base import BaseGenerator


class EquipmentGenerator(BaseGenerator):

    def __init__(self, equipment_info):
        super(EquipmentGenerator, self).__init__()
        self._equipment_infos = self.init(equipment_info)

    def get_create_list(self, result_mapping):
        return self._equipment_infos

    def create(self, equipment_info, result_mapping):
        equipment_qs = Equipment.query().filter(code = equipment_info.code)
        if equipment_qs.count():
            equipment = equipment_qs[0]
        else:
            equipment = Equipment.create(**equipment_info)
        return equipment

    def delete(self):
        print('======================>>> delete equipment <======================')
        return None
