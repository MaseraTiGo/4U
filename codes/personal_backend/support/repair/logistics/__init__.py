# coding=UTF-8

import json

from model.store.model_equipment import Equipment
from model.store.model_logistics import Logistics, LogisticsItem


class LogisticsRepair():

    '''
    def run(self):
        self.ready()
        i = 0
        logistics_item_qs = LogisticsItem.query().filter(create_time__gte = '2018-07-11 00:00:00')
        print("==========物流详情数：", len(logistics_item_qs))

        for logistics_item in logistics_item_qs:
            i = i + 1
            if i % 1000 == 0:
                print("=========>>>>>>>处理:", i)

            if logistics_item.id in self._all_equipment:
                equipment_list = self._all_equipment[logistics_item.id]
                equipment_sns = json.loads(logistics_item.equipment_sn_list)
                for equipment in equipment_list:
                    equipment_sns.append(equipment.code)
                equipment_sn_list = json.dumps(equipment_sns)
                logistics_item.update(equipment_sn_list = equipment_sn_list)


    def ready(self):
        self._all_equipment = {}
        equipment_qs = Equipment.query()
        print("=====设备数据数=====", len(equipment_qs))
        for equipment in equipment_qs:
            if equipment.logistics_item:
                if equipment.logistics_item_id not in self._all_equipment:
                    self._all_equipment[equipment.logistics_item_id] = [equipment]
                else:
                    self._all_equipment[equipment.logistics_item_id].append(equipment)

        print("=====数据准备完成=====")
    '''

    def run(self):
        self.ready()

        i = 0
        n = 0
        for key, value in self._all_logistics.items():
            i = i + 1
            if i % 1000 == 0:
                print("=========>>>>>>>logistics去重处理:", i)

            # service_list = self._all_service.get(order, None)

            # service_only = None
            h = 0
            logistics_only = None
            if len(value) > 1:
                n = n + 1

                for item in value:
                    h = h + 1
                    if h == 1:
                        logistics_only = item
                    else:
                        LogisticsItem.query(logistics = item).update(logistics = logistics_only)
                        item.delete()


    def ready(self):
        print("====数据准备中====")
        self._all_logistics = {}

        logistics_qs = Logistics.query()
        print("=====物流单数=====", len(logistics_qs))
        for logistics in logistics_qs:
            if (logistics.order_id, logistics.number) not in self._all_logistics:
                self._all_logistics[(logistics.order_id, logistics.number)] = [logistics]
            else:
                self._all_logistics[(logistics.order_id, logistics.number)].append(logistics)

        print("=====数据准备完成=====")
