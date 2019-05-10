# coding=UTF-8

import json

from model.store.model_order import Order, OrderItem
from model.store.model_logistics import LogisticsItem


class OrderItemRepair():


    def run(self):
        self.ready()

        i = 0
        n = 0
        for key, value in self._all_order_item.items():
            i = i + 1
            if i % 1000 == 0:
                print("=========>>>>>>>order_item去重处理:", i)

            # service_list = self._all_service.get(order, None)

            # service_only = None
            h = 0
            order_item_only = None
            if len(value) > 1:
                n = n + len(value)

                for item in value:
                    h = h + 1
                    if h == 1:
                        order_item_only = item
                    else:
                        LogisticsItem.query(order_item = item).update(order_item = order_item_only)
                        item.delete()



    def ready(self):
        print("====数据准备中====")

        self._all_order_item = {}

        order_item_qs = OrderItem.search()
        print("=====订单详情数=====", len(order_item_qs))
        for order_item in order_item_qs:
            if (order_item.order_id, order_item.goods_id) not in self._all_order_item:
                self._all_order_item[(order_item.order_id, order_item.goods_id)] = [order_item]
            else:
                self._all_order_item[(order_item.order_id, order_item.goods_id)].append(order_item)

        print("=====数据准备完成=====")
