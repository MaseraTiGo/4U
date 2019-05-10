# coding=UTF-8

from support.transfer.base import BaseTransfer
from model.store.model_mobilephone import MobileDevices, MobileMaintain


class MobileMaintainTransfer(BaseTransfer):

    def base_sql(self):
        if not hasattr(self, '_sql_str'):
            self._sql_str = "select a.create_date,a.modify_date,a.code,b.name as staff_name from ct_mobilecode a left join ct_admin b \
            ON a.adminid = b.id"

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
        print("==================成功结束MobileMaintain==================")

    def generate_date(self, data_list):
        for dic_data in data_list:
            mobile_devices = self.get_mobile_devices(dic_data["code"])
            staff = self.get_staff_byname(dic_data["staff_name"])
            if mobile_devices is not None and staff is not None:
                if self.skip_mobile_maintain(mobile_devices, staff):
                    MobileMaintain.create(devices = mobile_devices, staff = staff, \
                                          update_time = dic_data["modify_date"], create_time = dic_data["create_date"])

    def generate_sql(self, current, limit = 100):
        return "{s} limit {i},{l}".format(s = self._sql_str, i = current * limit, l = limit)

    def get_mobile_devices(self, code):
        mobile_devices_qs = MobileDevices.search(code = code)
        if mobile_devices_qs.count() > 0:
            return mobile_devices_qs[0]

        return None

    def skip_mobile_maintain(self, mobile_devices, staff):
        mobile_maintain_qs = MobileMaintain.search(devices = mobile_devices, staff = staff)
        if mobile_maintain_qs.count() == 0:
            return True

        return False

