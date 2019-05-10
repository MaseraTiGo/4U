# coding=UTF-8
import time
import json

from model.store.model_order import Order, OrderItem
from model.store.model_logistics import LogisticsItem


class OrderItemPriceRepair():


    def run(self):
        # self.ready()

        i = 0
        fb = open('/usr/src/app/support/temp_data.json', 'r')
        dicts = json.load(fb)
        fb.close()

        for key, value in dicts.items():
            length_value = len(value)
            if length_value > 10000:
                print(key)
                print(value)
                print("==总长度", length_value)
                n = 0
                s = length_value // 10000
                while n <= s:
                    start_index = n * 10000
                    if n == s:
                        end_index = length_value
                    else:
                        end_index = (n + 1) * 10000
                    print("=========", start_index, end_index)
                    value_section = value[start_index:end_index]
                    OrderItem.search(id__in = value_section).update(price = int(key))
                    n = n + 1
            else:
                OrderItem.search(id__in = value).update(price = int(key))


    def ready(self):

        print("====数据准备中====")

        self._all_order_item = {}

        order_item_qs = OrderItem.search()
        print("====订单详情数====", len(order_item_qs))
        for order_item in order_item_qs:
            self._all_order_item[order_item.id] = order_item

        print("====数据准备完成====")

