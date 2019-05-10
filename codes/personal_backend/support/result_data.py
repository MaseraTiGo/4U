# coding=UTF-8

import init_envt
import json
import time
import csv

from django.db.models import *

from model.store.model_order_event import StaffOrderEvent
from model.store.model_equipment_sn import EquipmentSn
from model.store.model_equipment_register import EquipmentRegister
from model.store.model_equipment_transaction import EquipmentTransaction


class ResultDataManager():

    def run(self):

        print("==开始==")
        department_list = [7, 32, 33, 47]
        staff_list_mapping = {}
        staff_order_event_qs = StaffOrderEvent.search(department_id__in = department_list)
        print("========order_event=======", staff_order_event_qs.count())
        for staff_order_event in staff_order_event_qs:
            if staff_order_event.staff_id not in staff_list_mapping:
                staff_list_mapping[staff_order_event.staff_id] = {}
                staff_list_mapping[staff_order_event.staff_id]["name"] = staff_order_event.staff.name
                staff_list_mapping[staff_order_event.staff_id]["order_ids"] = []
                staff_list_mapping[staff_order_event.staff_id]["order_ids"].append(staff_order_event.order_id)
            else:
                staff_list_mapping[staff_order_event.staff_id]["order_ids"].append(staff_order_event.order_id)
        print("====订单查询准备完成====", staff_list_mapping)

        num = 4
        i = 0
        while i < num:
            print("========i========", i)
            if i == 0:
                key_str = "2018-04"
                time_start = "2018-04-01 00:00:00"
                time_end = "2018-04-30 23:59:59"
            elif i == 1:
                key_str = "2018-05"
                time_start = "2018-05-01 00:00:00"
                time_end = "2018-05-31 23:59:59"
            elif i == 2:
                key_str = "2018-06"
                time_start = "2018-06-01 00:00:00"
                time_end = "2018-06-30 23:59:59"
            elif i == 3:
                key_str = "2018-07"
                time_start = "2018-07-01 00:00:00"
                time_end = "2018-07-31 23:59:59"
            for key, value in staff_list_mapping.items():
                print("========name========", value["name"], time_start, len(value["order_ids"]))
                equipment_sn_qs = EquipmentSn.search(order_id__in = value["order_ids"], \
                                                     order__pay_time__range = (time_start, time_end))
                equipment_sn_list = []
                for equipment_sn in equipment_sn_qs:
                    equipment_sn_list.append(equipment_sn.id)

                equipment_register_qs = EquipmentRegister.search(equipment_sn_id__in = equipment_sn_list)

                staff_list_mapping[key][key_str] = {}
                staff_list_mapping[key][key_str]["sn_count"] = equipment_sn_qs.count()
                staff_list_mapping[key][key_str]["sn_register_count"] = equipment_register_qs.count()

                equipment_register_list = []
                for equipment_register in equipment_register_qs:
                    equipment_register_list.append(equipment_register.id)

                n = 0
                while n < num:
                    print("========i========", i)
                    if n == 0:
                        cal_str = "2018-04"
                        time_start_cal = "2018-04-01 00:00:00"
                        time_end_cal = "2018-04-30 23:59:59"
                    elif n == 1:
                        cal_str = "2018-05"
                        time_start_cal = "2018-05-01 00:00:00"
                        time_end_cal = "2018-05-31 23:59:59"
                    elif n == 2:
                        cal_str = "2018-06"
                        time_start_cal = "2018-06-01 00:00:00"
                        time_end_cal = "2018-06-30 23:59:59"
                    elif n == 3:
                        cal_str = "2018-07"
                        time_start_cal = "2018-07-01 00:00:00"
                        time_end_cal = "2018-07-31 23:59:59"
                    equipment_transaction_qs = EquipmentTransaction.search(code_id__in = equipment_register_list, \
                                                                           transaction_time__range = (time_start_cal, time_end_cal))
                    print("====changdu====", equipment_transaction_qs.count())
                    transaction_sum = equipment_transaction_qs.aggregate(sum_transaction_money = Sum('transaction_money'))
                    print("====sum====", transaction_sum)

                    staff_list_mapping[key][key_str][cal_str] = transaction_sum["sum_transaction_money"] if transaction_sum["sum_transaction_money"] else 0
                    n = n + 1

            i = i + 1

        csvFile3 = open('baobiao2222.csv', 'w', newline = '')
        writer2 = csv.writer(csvFile3)
        writer2.writerow(['姓名', '四月单量', '四月开通量', '四月开通人四月流水', '四月开通人五月流水', '四月开通人六月流水', '四月开通人七月流水', \
                         '五月单量', '五月开通量', '五月开通人四月流水', '五月开通人五月流水', '五月开通人六月流水', '五月开通人七月流水', \
                         '六月单量', '六月开通量', '六月开通人四月流水', '六月开通人五月流水', '六月开通人六月流水', '六月开通人七月流水', \
                         '七月单量', '七月开通量', '七月开通人四月流水', '七月开通人五月流水', '七月开通人六月流水', '七月开通人七月流水'])
        for key, value in staff_list_mapping.items():
            item = [value["name"], value["2018-04"]["sn_count"], value["2018-04"]["sn_register_count"], value["2018-04"]["2018-04"], \
                    value["2018-04"]["2018-05"], value["2018-04"]["2018-06"], value["2018-04"]["2018-07"], \
                    value["2018-05"]["sn_count"], value["2018-05"]["sn_register_count"], value["2018-05"]["2018-04"], \
                    value["2018-05"]["2018-05"], value["2018-05"]["2018-06"], value["2018-05"]["2018-07"], \
                    value["2018-06"]["sn_count"], value["2018-06"]["sn_register_count"], value["2018-06"]["2018-04"], \
                    value["2018-06"]["2018-05"], value["2018-06"]["2018-06"], value["2018-06"]["2018-07"], \
                    value["2018-07"]["sn_count"], value["2018-07"]["sn_register_count"], value["2018-07"]["2018-04"], \
                    value["2018-07"]["2018-05"], value["2018-07"]["2018-06"], value["2018-07"]["2018-07"]]
            writer2.writerow(item)
        csvFile3.close()

        print("====result====", staff_list_mapping)

if __name__ == "__main__":
    ResultDataManager().run()
