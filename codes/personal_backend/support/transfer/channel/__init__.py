# coding=UTF-8

from support.transfer.base import BaseTransfer
from model.store.model_shop import Channel

class ChannelTransfer(BaseTransfer):

    def base_sql(self):
        if not hasattr(self, '_sql_str'):
            self._sql_str = "select * from ct_sale_channel where grade=0 and create_date between '2018-06-21 00:00:00' \
            and '2018-06-21 23:59:59'"

    def run(self):
        self.base_sql()
        current = 0
        sql = self.generate_sql(current)
        data_list = self.get_date_list(sql)
        print("============", sql)
        while len(data_list) > 0:
            print("============", len(data_list))
            channel_list = self.generate_date(data_list)
            Channel.objects.bulk_create(channel_list)
            current = current + 1
            sql = self.generate_sql(current)
            data_list = self.get_date_list(sql)

        self.break_link()
        print("==================成功结束Channel==================")

    def generate_date(self, data_list):
        channel_list = []
        for dic_data in data_list:
            channel_qs = Channel.search(name = dic_data["name"])
            if channel_qs.count() == 0:
                channel_list.append(Channel(name = dic_data["name"], freight = 900, \
                                            single_repair_money = int(dic_data["remoney"] * 100) if dic_data["remoney"] else 0, \
                                            single_point_money = int(dic_data['bucmoney'] * 100) if dic_data["bucmoney"] else 0, \
                                            update_time = dic_data["modify_date"], \
                                            create_time = dic_data["create_date"]))

        return channel_list

    def generate_sql(self, current, limit = 100):
        return "{s} limit {i},{l}".format(s = self._sql_str, i = current * limit, l = limit)

