# coding=UTF-8

import json

from model.store.model_equipment import Equipment
from model.store.model_logistics import Logistics, LogisticsItem


class LogisticsItemRepair():


    def run(self):
        self.ready()

        i = 0
        n = 0
        for key, value in self._all_logistics_item.items():
            i = i + 1
            if i % 1000 == 0:
                print("=========>>>>>>>logistics_item去重处理:", i)

            # service_list = self._all_service.get(order, None)

            # service_only = None
            h = 0
            logistics_item_only = None
            if len(value) > 1:
                n = n + len(value)

                for item in value:
                    h = h + 1
                    if h == 1:
                        logistics_item_only = item
                    else:
                        Equipment.query(logistics_item = item).update(logistics_item = logistics_item_only)
                        self.handle_sn(logistics_item_only, item)
                        item.delete()


    def ready(self):
        print("====数据准备中====")
        self._all_logistics_item = {}

        logistics_item_qs = LogisticsItem.query()
        print("=====物流单详情数=====", len(logistics_item_qs))
        for logistics_item in logistics_item_qs:
            if (logistics_item.logistics_id, logistics_item.order_item_id) not in self._all_logistics_item:
                self._all_logistics_item[(logistics_item.logistics_id, logistics_item.order_item_id)] = [logistics_item]
            else:
                self._all_logistics_item[(logistics_item.logistics_id, logistics_item.order_item_id)].append(logistics_item)

        print("=====数据准备完成=====")

    def handle_sn(self, logistics_item_only, logistics_item):
        equipment_only_sns = json.loads(logistics_item_only.equipment_sn_list)
        equipment_sns = json.loads(logistics_item.equipment_sn_list)
        equipment_only_sns = list(set(equipment_only_sns + equipment_sns))
        equipment_sn_list = json.dumps(equipment_only_sns)
        logistics_item_only.update(equipment_sn_list = equipment_sn_list)
