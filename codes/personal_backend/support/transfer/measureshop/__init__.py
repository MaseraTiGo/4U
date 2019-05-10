# coding=UTF-8

from support.transfer.base import BaseTransfer
from model.store.model_measure_shop import MeasureShop
from model.store.model_shop import Shop


class MeasureShopTransfer(BaseTransfer):

    def base_sql(self):
        if not hasattr(self, '_sql_str'):
            self._sql_str = "select *,b.name as staff_name,c.name as shop_name from ct_sales_report a left join ct_admin \
            b ON a.adminid= b.id left join ct_sale_channel c ON a.saleid=c.id"

    def run(self):
        print("进入")
        self.base_sql()
        current = 0
        sql = self.generate_sql(current)
        data_list = self.get_date_list(sql)
        print("============", sql)
        while len(data_list) > 0:
            print("============", len(data_list))
            measure_shop_list = self.generate_date(data_list)
            MeasureShop.objects.bulk_create(measure_shop_list)
            current = current + 1
            sql = self.generate_sql(current)
            data_list = self.get_date_list(sql)

        self.break_link()
        print("==================成功结束MeasureShop==================")

    def generate_date(self, data_list):
        measure_shop_list = []
        for dic_data in data_list:
            shop = self.get_shop(dic_data["shop_name"])
            measure_shop_list.append(MeasureShop(staff = self.get_staff_byname(dic_data["staff_name"]), shop = shop, \
                                                 total_sales = dic_data["totalnum"], add_order_number = dic_data["repairnum"], \
                                                 add_order_per_money = shop.single_repair_money, add_order_total_money = int(dic_data["repairmoney"] * 100), \
                                                 single_point_per_money = shop.single_point_money, single_point_total_money = int(dic_data["points"] * 100), \
                                                 through_number = dic_data["throughnum"], through_money = int(dic_data["throughmoney"] * 100), \
                                                 freight = shop.freight, total_freight = int(dic_data["freight"] * 100), record_date = dic_data["record_date"], \
                                                 update_time = dic_data["modify_date"], create_time = dic_data["create_date"]))

        return measure_shop_list

    def generate_sql(self, current, limit = 100):
        return "{s} limit {i},{l}".format(s = self._sql_str, i = current * limit, l = limit)

    def get_shop(self, shop_name):
        return Shop.get_shop_buyname(name = shop_name)

