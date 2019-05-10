# coding=UTF-8

from support.transfer.base import BaseTransfer
from model.store.model_equipment_out import EquipmentOut


class EquipmentoutTransfer(BaseTransfer):

    def base_sql(self):
        if not hasattr(self, '_sql_str'):
            self._sql_str = "select * from ct_sn_out"

    def run(self):
        self.base_sql()
        current = 0
        sql = self.generate_sql(current)
        data_list = self.get_date_list(sql)
        print("============", sql)
        while len(data_list) > 0:
            print("============", len(data_list))
            equipmentout_list = self.generate_date(data_list)
            EquipmentOut.objects.bulk_create(equipmentout_list)
            current = current + 1
            sql = self.generate_sql(current)
            data_list = self.get_date_list(sql)

        self.break_link()
        print("==================成功结束Equipmentout==================")

    def generate_date(self, data_list):
        equipmentout_list = []
        for dic_data in data_list:
            equipmentout_list.append(EquipmentOut(add_time = dic_data["adddate"], agent_name = dic_data["agent_name"], agent_phone = dic_data["mobile"], \
                                                  product_type = dic_data["product_type"], product_model = dic_data["product_model"].upper(), \
                                                  min_number = dic_data["min_number"], max_number = dic_data["max_number"], quantity = dic_data["number"], \
                                                  price = dic_data["per_price"], salesman = dic_data["salesman"], address = dic_data["address"], \
                                                  rate = dic_data["rate"], remark = dic_data["remarks"], update_time = dic_data["modify_date"], \
                                                  create_time = dic_data["create_date"]))
        return equipmentout_list

    def generate_sql(self, current, limit = 100):
        return "{s} limit {i},{l}".format(s = self._sql_str, i = current * limit, l = limit)
