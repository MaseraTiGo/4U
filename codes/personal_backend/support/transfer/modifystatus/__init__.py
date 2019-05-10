# coding=UTF-8

from support.transfer.base import BaseTransfer
from model.store.model_equipment import Equipment
from model.store.model_equipment_register import EquipmentRegister
from model.store.model_service import ServiceItem


class ModifystatusTransfer(BaseTransfer):

    def base_sql(self):
        if not hasattr(self, '_sql_str'):
            self._sql_str = "select create_date,modify_date,name,register_id,terminal_code,sn_color,\
            agent_name,customer_code,customer_createtime,customer_bindtime,rebate_color from ct_channel_user where is_dsinfo=1 \
            and customer_bindtime between '2018-06-01 00:00:00' and '2018-06-20 23:59:59'"

    def run(self):
        self.base_sql()
        current = 0
        count = 0
        sql = self.generate_sql(current)
        data_list = self.get_date_list(sql)
        print("============", sql)
        while len(data_list) > 0:
            count += len(data_list)
            print("start to deal data for items :  count --> ", count)
            self.generate_date(data_list)
            # EquipmentRegister.objects.bulk_create(register_list)
            current = current + 1
            sql = self.generate_sql(current)
            data_list = self.get_date_list(sql)

        self.break_link()
        print("==================成功结束==================")

    def generate_date(self, data_list):
        for dic_data in data_list:
            service_item = self.skip_register(dic_data["terminal_code"])
            if service_item is not None:
                service_item.update(dsinfo_status = "yellow", rebate_status = self.get_rebate_status(dic_data["rebate_color"]))


    def generate_sql(self, current, limit = 100):
        return "{s} limit {i},{l}".format(s = self._sql_str, i = current * limit, l = limit)


    def skip_register(self, terminal_code):
        service_item = None
        service_item_qs = ServiceItem.search(equipment__code = terminal_code)
        if service_item_qs.count() > 0:
            service_item = service_item_qs[0]

        return service_item

    def check_equipment(self, terminal_code):
        equipment = None
        equipment_qs = Equipment.search(code = terminal_code)
        if equipment_qs.count() > 0:
            equipment = equipment_qs[0]

        return equipment

    def get_rebate_status(self, sn_color):
        rebate_status = sn_color
        if sn_color == "green":
            rebate_status = "tgreen"
        elif sn_color == "green1":
            rebate_status = "green"

        return rebate_status
