# coding=UTF-8

import json

from model.store.model_order import Order, OrderItem


class OrderRepair():


    def run(self):
        self.ready()

        i = 0
        order_qs = Order.search()
        print("==========订单数：", len(order_qs))

        for order in order_qs:
            i = i + 1
            if i % 1000 == 0:
                print("=========>>>>>>>order金额处理:", i)

            total_price = 0
            total_quantity = 0
            if order.id in self._all_order_item:
                order_item_list = self._all_order_item[order.id]
                for order_item in order_item_list:
                    total_price = total_price + order_item.price * order_item.quantity
                    total_quantity = total_quantity + order_item.quantity

                if total_price != order.total_price or total_quantity != order.total_quantity:
                    order.update(total_price = total_price, total_quantity = total_quantity)


    def ready(self):
        print("====数据准备中====")
        self._all_order_item = {}
        order_item_qs = OrderItem.query()
        print("=====订单详情数据数=====", len(order_item_qs))
        for order_item in order_item_qs:
            if order_item.order_id not in self._all_order_item:
                self._all_order_item[order_item.order_id] = [order_item]
            else:
                self._all_order_item[order_item.order_id].append(order_item)

        print("=====数据准备完成=====")

