# coding=UTF-8

import json

from support.transfer.base import BaseTransfer
from model.store.model_order import Order, OrderItem
from model.store.model_shop import Goods


class OrderTransfer(BaseTransfer):

    def base_sql(self):
        self._n = 0
        self._order_item_mapping_all = {}
        if not hasattr(self, '_sql_str'):
            self._sql_str = "select * from ct_channel_user"


    def run(self):
        self.ready()
        self.base_sql()
        current = 0
        count = 0
        sql = self.generate_sql(current)
        data_list = self.get_date_list(sql)
        print("============", sql)
        while len(data_list) > 0:
            count += len(data_list)
            print("start to deal data for buy_price :  count --> ", count)

            self.generate_date(data_list)

            current = current + 1
            sql = self.generate_sql(current)
            data_list = self.get_date_list(sql)

        self.break_link()
        print("==========", self._order_item_mapping_all)

        print("==================成功结束Channel=356==================", len(self._order_item_mapping_all))
        with open('./support/temp_data.json', 'w') as f:
                f.write(json.dumps(self._order_item_mapping_all))
                f.close()


    def generate_date(self, data_list):
        for dic_data in data_list:
            order_sn = ""
            order = None
            goods = None

            if dic_data["order_id"]:
                order_sn = dic_data["order_id"]
            else:
                order_sn = dic_data["document_number"]

            if dic_data["buy_price"] and order_sn and dic_data["product_name"]:
                if order_sn in self._all_order:
                    order = self._all_order[order_sn]

                if dic_data["product_name"] in self._all_goods:
                    goods = self._all_goods[dic_data["product_name"]]

                if order is not None and goods is not None:
                    if (order.id, goods.id) in self._all_order_item:
                        order_item = self._all_order_item[(order.id, goods.id)]
                        buy_price = int(dic_data["buy_price"] * 100)
                        if order_item.price != buy_price:
                            if str(buy_price) in self._order_item_mapping_all:
                                self._order_item_mapping_all[str(buy_price)].append(order_item.id)
                            else:
                                self._order_item_mapping_all[str(buy_price)] = [order_item.id]
                            '''
                            order_item_mapping = {}
                            order_item_mapping.update({"order_id":order.id, "goods_id":goods.id, "buy_price":str(dic_data["buy_price"] * 100)})
                            self._n = self._n + 1
                            self._order_item_mapping_all[self._n] = order_item_mapping
                            # order_item.update(price = dic_data["buy_price"] * 100)
                            '''

    def generate_sql(self, current, limit = 100):
        return "{s} limit {i},{l}".format(s = self._sql_str, i = current * limit, l = limit)


    def ready(self):
        print("====数据准备中====")
        self._all_order = {}
        self._all_order_item = {}
        self._all_goods = {}

        order_qs = Order.search()
        print("====订单数====", len(order_qs))
        for order in order_qs:
            self._all_order[order.order_sn] = order

        order_item_qs = OrderItem.search()
        print("====订单详情数====", len(order_item_qs))
        for order_item in order_item_qs:
            self._all_order_item[(order_item.order_id, order_item.goods_id)] = order_item

        goods_qs = Goods.query()
        print("====商品数====", len(goods_qs))
        for goods in goods_qs:
            self._all_goods[goods.name] = goods

        print("====数据准备完成====")
