# coding=UTF-8

from support.transfer.base import BaseTransfer
from model.store.model_shop import Shop, Channel

class ShopTransfer(BaseTransfer):

    def base_sql(self):
        if not hasattr(self, '_sql_str'):
            self._sql_str = "select *,b.name as channle_name from ct_sale_channel a left join ct_sale_channel \
            b ON a.parent_id= b.id where a.grade=1 and a.create_date between '2018-06-21 00:00:00' \
            and '2018-06-21 23:59:59'"

    def run(self):
        self.base_sql()
        current = 0
        sql = self.generate_sql(current)
        data_list = self.get_date_list(sql)
        print("============", sql)
        while len(data_list) > 0:
            print("============", len(data_list))
            shop_list = self.generate_date(data_list)
            Shop.objects.bulk_create(shop_list)
            current = current + 1
            sql = self.generate_sql(current)
            data_list = self.get_date_list(sql)

        self.break_link()
        print("==================成功结束Shop==================")

    def generate_date(self, data_list):
        shop_list = []
        for dic_data in data_list:
            shop = Shop.get_shop_buyname(name = dic_data["name"])
            if shop is None:
                shop_list.append(Shop(channel = self.get_channel(dic_data["channle_name"]), name = dic_data["name"], freight = 900, \
                                      single_repair_money = int(dic_data["remoney"] * 100), single_point_money = int(dic_data["bucmoney"] * 100), \
                                      is_distribution = self.get_is_distribution(dic_data["isdistribution"]), update_time = dic_data["modify_date"], \
                                      create_time = dic_data["create_date"]))

        return shop_list

    def generate_sql(self, current, limit = 100):
        return "{s} limit {i},{l}".format(s = self._sql_str, i = current * limit, l = limit)


    def get_channel(self, channel_name):
        channel_qs = Channel.search(name = channel_name)
        if channel_qs.count() > 0:
            return channel_qs[0]

        return None

    def get_is_distribution(self, value):
        if int(value) > 0:
            return True
        else:
            return False
