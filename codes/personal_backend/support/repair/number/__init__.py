# coding=UTF-8

import json

from django.db.models import *

from model.store.model_order import Order, OrderItem
from model.store.model_logistics import Logistics, LogisticsItem


class NumberRepair():


    def run(self):
        print("====数据准备中====")
        self.repair_logistics_item()
        self.repair_logistics()
        self.repair_order_item()
        self.repair_order()

    def repair_logistics_item(self):

        logistics_item_qs = LogisticsItem.query()
        i = 0
        print("==========物流详情数：", len(logistics_item_qs))
        for logistics_item in logistics_item_qs:
            i = i + 1
            if i % 1000 == 0:
                print("=========>>>>>>>logistics_item数量处理:", i)
            equipment_sns = json.loads(logistics_item.equipment_sn_list)
            if logistics_item.quantity != len(equipment_sns):
                logistics_item.update(quantity = len(equipment_sns))

        print("=====repair_logistics_item==完成=====")


    def  repair_logistics(self):
        _all_logistics_item = {}

        logistics_item_qs = LogisticsItem.query()
        print("=====物流单详情数=====", len(logistics_item_qs))

        for logistics_item in logistics_item_qs:
            if logistics_item.logistics_id not in _all_logistics_item:
                _all_logistics_item[logistics_item.logistics_id] = [logistics_item]
            else:
                _all_logistics_item[logistics_item.logistics_id].append(logistics_item)

        print("=====数据准备完成=====")

        logistics_qs = Logistics.query()
        i = 0
        for logistics in logistics_qs:
            i = i + 1
            if i % 1000 == 0:
                print("=========>>>>>>>logistics数量处理:", i)
            if logistics.id in _all_logistics_item:
                num = 0
                for item in _all_logistics_item[logistics.id]:
                    num = num + item.quantity
                if logistics.total_quantity != num:
                    logistics.update(total_quantity = num)


    def repair_order_item(self):
        _all_logistics_item = {}

        logistics_item_qs = LogisticsItem.query()
        print("=====物流单详情数=====", len(logistics_item_qs))

        for logistics_item in logistics_item_qs:
            if logistics_item.order_item_id not in _all_logistics_item:
                _all_logistics_item[logistics_item.order_item_id] = [logistics_item]
            else:
                _all_logistics_item[logistics_item.order_item_id].append(logistics_item)

        print("=====数据准备完成=====")

        order_item_qs = OrderItem.search()
        i = 0
        for order_item in order_item_qs:
            i = i + 1
            if i % 1000 == 0:
                print("=========>>>>>>>order_item数量处理:", i)
            if order_item.id in _all_logistics_item:
                num = 0
                for item in _all_logistics_item[order_item.id]:
                    num = num + item.quantity
                if order_item.quantity != num:
                    order_item.update(quantity = num)


    def repair_order(self):

        _all_order_item = {}

        order_item_qs = OrderItem.search()
        print("=====订单详情数=====", len(order_item_qs))

        for order_item in order_item_qs:
            if order_item.order_id not in _all_order_item:
                _all_order_item[order_item.order_id] = [order_item]
            else:
                _all_order_item[order_item.order_id].append(order_item)

        print("=====数据准备完成=====")

        order_qs = Order.search()
        i = 0
        for order in order_qs:
            i = i + 1
            if i % 1000 == 0:
                print("=========>>>>>>>order数量处理:", i)
            if order.id in _all_order_item:
                num = 0
                for item in _all_order_item[order.id]:
                    num = num + item.quantity
                if order.total_quantity != num:
                    order.update(total_quantity = num)
