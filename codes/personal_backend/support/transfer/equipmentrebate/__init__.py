# coding=UTF-8
import datetime

from support.transfer.base import BaseTransfer
from model.store.model_equipment_register import EquipmentRegister
from model.store.model_equipment_rebate import EquipmentRebate
from model.store.model_import import ImportCustomerRebate


class EquipmentRebateTransfer(BaseTransfer):

    def base_sql(self):
        if not hasattr(self, '_sql_str'):
            self._sql_str = "select * from ct_rebate where month between '2018-06-15 00:00:00' and '2018-06-20 23:59:59'"


    def run(self):
        self.base_sql()
        current = 0
        count = 0
        sql = self.generate_sql(current)
        print("============", sql)
        data_list = self.get_date_list(sql)
        while len(data_list) > 0:
            count += len(data_list)
            print("start to deal data for items :  count --> ", count)
            rebate_list, import_rebate_list = self.generate_date(data_list)
            if len(rebate_list) > 0:
                EquipmentRebate.objects.bulk_create(rebate_list)
            if len(import_rebate_list) > 0:
                ImportCustomerRebate.objects.bulk_create(import_rebate_list)
            current = current + 1
            sql = self.generate_sql(current)
            data_list = self.get_date_list(sql)

        self.break_link()
        print("==================成功结束==================")

    def generate_date(self, data_list):
        rebate_list = []
        import_rebate_list = []
        customer_ids = []
        customer_ids = [dic_data["customer_id"] for dic_data in data_list]

        register_mapping = {equipment_register.code:equipment_register for equipment_register in \
                          EquipmentRegister.search(code__in = customer_ids)}

        for dic_data in data_list:
            register = register_mapping.get(dic_data["customer_id"], None)
            if register is None:
                import_rebate_list.append(ImportCustomerRebate(agent_id = dic_data["agent_id"], agent_name = dic_data["agent_name"], \
                                                       name = dic_data["name"], phone = dic_data["mobile"], \
                                                       code = dic_data["customer_id"], \
                                                       register_time = self.tranger_time(dic_data["regist_time"]) if dic_data["regist_time"] else None,
                                                       bind_time = self.tranger_time(dic_data["bind_time"]) if dic_data["bind_time"] else None, \
                                                       month = dic_data["month"], \
                                                       transaction_amount = int(dic_data["money"] * 100) if dic_data["money"] else 0, \
                                                       effective_amount = int(dic_data["effective_money"] * 100) if dic_data["effective_money"] else 0, \
                                                       accumulate_amount = int(dic_data["last_money"] * 100) if dic_data["last_money"] else 0, \
                                                       history_amount = int(dic_data["alllast_money"] * 100) if dic_data["alllast_money"] else 0, \
                                                       type = dic_data["type"], is_rebate = dic_data["is_rebate"], remark = dic_data["remarks"], \
                                                       update_time = dic_data["modify_date"], create_time = dic_data["create_date"], \
                                                       status = "failed", error_text = "客户编码无法匹配"))
            else:
                rebate_list.append(EquipmentRebate(agent_id = dic_data["agent_id"], agent_name = dic_data["agent_name"], code = register, \
                                                   name = dic_data["name"], phone = dic_data["mobile"], \
                                                   register_code = dic_data["customer_id"], \
                                                   register_time = self.tranger_time(dic_data["regist_time"]) if dic_data["regist_time"] else None,
                                                   bind_time = self.tranger_time(dic_data["bind_time"]) if dic_data["bind_time"] else None, \
                                                   month = dic_data["month"], \
                                                   transaction_amount = int(dic_data["money"] * 100) if dic_data["money"] else 0, \
                                                   effective_amount = int(dic_data["effective_money"] * 100) if dic_data["effective_money"] else 0, \
                                                   accumulate_amount = int(dic_data["last_money"] * 100) if dic_data["last_money"] else 0, \
                                                   history_amount = int(dic_data["alllast_money"] * 100) if dic_data["alllast_money"] else 0, \
                                                   type = dic_data["type"], is_rebate = dic_data["is_rebate"], remark = dic_data["remarks"], \
                                                   update_time = dic_data["modify_date"], create_time = dic_data["create_date"]))
        return rebate_list, import_rebate_list


    def check_data(self, dic_data):
        equipment_rebate_qs = EquipmentRebate.search(register_code = dic_data["customer_id"], month = dic_data["month"])
        if equipment_rebate_qs.count() > 0:
            print("=====去重复")
            return False
        return True

    def generate_sql(self, current, limit = 100):
        return "{s} limit {i},{l}".format(s = self._sql_str, i = current * limit, l = limit)


    def tranger_time(self, strtime):
        value_time = datetime.datetime.strptime(strtime.strip(), '%Y%m%d')
        value_time_day = datetime.date(value_time.year, value_time.month, value_time.day)

        return value_time_day
