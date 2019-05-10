# coding=UTF-8

from support.transfer.base import BaseTransfer
from model.store.model_mobilephone import MobileDevices


class MobileDevicesTransfer(BaseTransfer):

    def base_sql(self):
        if not hasattr(self, '_sql_str'):
            self._sql_str = "select * from ct_mobilecode"

    def run(self):
        print("进入")
        self.base_sql()
        current = 0
        sql = self.generate_sql(current)
        data_list = self.get_date_list(sql)
        print("============", sql)
        while len(data_list) > 0:
            print("============", len(data_list))
            self.generate_date(data_list)
            current = current + 1
            sql = self.generate_sql(current)
            data_list = self.get_date_list(sql)

        self.break_link()
        print("==================成功结束MobileDevices==================")

    def generate_date(self, data_list):
        for dic_data in data_list:
            if self.skip_mobile_devices(dic_data["code"]):
                MobileDevices.create(code = dic_data["code"], remark = dic_data["remark"], \
                              update_time = dic_data["modify_date"], create_time = dic_data["create_date"])

    def generate_sql(self, current, limit = 100):
        return "{s} limit {i},{l}".format(s = self._sql_str, i = current * limit, l = limit)

    def skip_mobile_devices(self, code):
        mobile_devices_qs = MobileDevices.search(code = code)
        if mobile_devices_qs.count() == 0:
            return True

        return False

