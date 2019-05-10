# coding=UTF-8

'''
Created on 2016年7月22日

@author: Administrator
'''

import hashlib
import datetime
import json
import random
from tuoen.sys.utils.common.timetools import add_month
from django.db.models import *

from tuoen.sys.core.exception.business_error import BusinessError
from tuoen.sys.utils.common.split_page import Splitor
from tuoen.sys.utils.common.dictwrapper import DictWrapper

from tuoen.abs.middleware.department import department_middleware

from model.models import Service, ServiceItem
from model.store.model_equipment import EquipmentStatusType, EquipmentStatusState
from model.store.model_equipment_sn import SnStatusType, SnStatus
from model.models import AuthAccess, AccessTypes
from model.models import EquipmentSn, SnStatus, Equipment, EquipmentIn
from model.models import EquipmentRegister, EquipmentRebate
from model.models import LogisticsItem, EquipmentTransaction
from model.store.model_orderreturns import OrderReturns
from model.store.model_returnsevent import StaffReturnsEvent
from model.store.model_department import Department


class ServiceServer(object):

    @classmethod
    def search(cls, current_page, **search_info):
        """查询服务列表"""
        user_pro = search_info.pop('cur_user')
        service_qs = Service.search(**search_info)
        if not user_pro._is_show_sub:
            service_qs = service_qs.filter(seller_id__exact = user_pro._cur_user_id)
        if user_pro._is_admin:
            service_qs = Service.query()
        service_qs = service_qs.order_by("-create_time")
        return Splitor(current_page, service_qs)

    @classmethod
    def get(cls, service_id):
        """售后服务单信息"""
        service = Service.get_byid(service_id)
        if service is None:
            raise BusinessError("售后服务单不存在")

        return service

    @classmethod
    def hung_staff_forservice(cls, service_item_list):
        """售后服务单产品挂在客服"""
        service_id_list = []
        for service_item in service_item_list:
            if service_item.service:
                service_id_list.append(service_item.service.id)

        service_mapping = {}
        if len(service_id_list) > 0:
            service_mapping = {service.id: service for service in \
                               Service.search(id__in = service_id_list)}

        for service_item in service_item_list:
            service_item.pre_staff = None
            service_item.after_staff = None
            service_item.order = None
            if service_item.service:
                service = service_mapping.get(service_item.service.id, None)
                if service is not None:
                    service_item.pre_staff = service.seller
                    service_item.after_staff = service.server
                    service_item.order = service.order

        return service_item_list


class ServiceItemServer(object):

    @classmethod
    def search(cls, current_page, **search_info):
        """售后服务单产品列表查询"""

        service_item_qs = cls.search_qs(**search_info)
        service_item_qs = service_item_qs.order_by("-create_time")

        return Splitor(current_page, service_item_qs)

    @classmethod
    def alculation_by_searchinfo(cls, **search_info):
        sum_data = DictWrapper({})
        sum_data.volume_total = 0
        sum_data.open_number_total = 0
        sum_data.activation_number_total = 0
        sum_data.open_rate_total = "0%"
        sum_data.activation_rate_total = "0%"

        service_item_qs = cls.search_qs(**search_info)

        sum_data.volume_total = service_item_qs.filter(equipment_sn__sn_status = SnStatus.NORMAL). \
            aggregate(total_num = Count('id'))["total_num"]
        sum_data.open_number_total = service_item_qs.filter(equipment_sn__sn_status = SnStatus.NORMAL). \
            filter(~Q(dsinfo_status = SnStatusType.RED)).aggregate(total_num = Count('id'))["total_num"]
        sum_data.activation_number_total = service_item_qs.filter(equipment_sn__sn_status = SnStatus.NORMAL). \
            filter(~Q(rebate_status = SnStatusType.RED)).aggregate(total_num = Count('id'))["total_num"]

        if sum_data.volume_total > 0 and sum_data.open_number_total > 0:
            sum_data.open_rate_total = "{number}%".format(number = round((sum_data.open_number_total \
                                                                        / sum_data.volume_total) * 100, 2))

        if sum_data.volume_total > 0 and sum_data.activation_number_total > 0:
            sum_data.activation_rate_total = "{number}%".format(number = round((sum_data.activation_number_total \
                                                                              / sum_data.volume_total) * 100, 2))
        return sum_data

    @classmethod
    def search_qs(cls, **search_info):
        dsinfo_status = -1
        rebate_status = -1
        if "dsinfo_status" in search_info:
            dsinfo_status = search_info.pop("dsinfo_status")

        if "rebate_status" in search_info:
            rebate_status = search_info.pop("rebate_status")

        service_item_qs = ServiceItem.search(**search_info)

        if dsinfo_status == 0:
            service_item_qs = service_item_qs.filter(dsinfo_status = "red")
        elif dsinfo_status == 1:
            service_item_qs = service_item_qs.filter(~Q(dsinfo_status = 'red'))

        if rebate_status == 0:
            service_item_qs = service_item_qs.filter(rebate_status = "red")
        elif rebate_status == 1:
            service_item_qs = service_item_qs.filter(~Q(rebate_status = 'red'))

        return service_item_qs;

    @classmethod
    def get(cls, service_item_id):
        """售后服务单产品信息"""
        service_item = ServiceItem.get_byid(service_item_id)
        if service_item is None:
            raise BusinessError("售后服务单设备不存在")

        return service_item

    @classmethod
    def summing(cls, sum_data, **search_info):
        sum_measure_data = DictWrapper({})
        sum_measure_data.volume_total = 0
        sum_measure_data.open_number_total = 0
        sum_measure_data.activation_number_total = 0
        sum_measure_data.conversion_rate_total = "0%"
        sum_measure_data.open_rate_total = "0%"
        sum_measure_data.activation_rate_total = "0%"

        if 'cur_user' in search_info:
            user_pro = search_info.pop('cur_user')
            if not user_pro._is_admin:
                if "service__seller_id__in" in search_info:
                    search_info.update({"service__seller_id__in": list(
                        set(search_info["service__seller_id__in"]).intersection(set(user_pro._staff_id_list)))})
                else:
                    search_info.update({"service__seller_id__in": user_pro._staff_id_list})

        if "begin_time" in search_info:
            begin_time = search_info.pop("begin_time")
            search_info.update({"order__pay_time__gte": \
                                    datetime.datetime(begin_time.year, begin_time.month, begin_time.day, 0, 0, 0)})

        if "end_time" in search_info:
            end_time = search_info.pop("end_time")
            search_info.update({"order__pay_time__lte": \
                                    datetime.datetime(end_time.year, end_time.month, end_time.day, 23, 59, 59)})

        if "staff" in search_info:
            staff = search_info.pop("staff")
            search_info.update({"service__seller": staff})

        service_item_qs = cls.search_qs(**search_info)

        sum_measure_data.volume_total = service_item_qs.filter(equipment_sn__sn_status = SnStatus.NORMAL). \
            aggregate(total_num = Count('id'))["total_num"]
        sum_measure_data.open_number_total = service_item_qs.filter(equipment_sn__sn_status = SnStatus.NORMAL). \
            filter(~Q(dsinfo_status = EquipmentStatusType.RED)).aggregate(total_num = Count('id'))["total_num"]
        sum_measure_data.activation_number_total = service_item_qs.filter(equipment_sn__sn_status = SnStatus.NORMAL). \
            filter(~Q(rebate_status = SnStatusType.RED)).aggregate(total_num = Count('id'))["total_num"]

        if sum_data.new_number > 0 and sum_measure_data.volume_total > 0:
            sum_measure_data.conversion_rate_total = "{number}%".format(number = round((sum_measure_data.volume_total \
                                                                                      / sum_data.new_number) * 100, 2))

        if sum_measure_data.volume_total > 0 and sum_measure_data.open_number_total > 0:
            sum_measure_data.open_rate_total = "{number}%".format(number = round((sum_measure_data.open_number_total \
                                                                                / sum_measure_data.volume_total) * 100,
                                                                               2))

            sum_measure_data.activation_rate_total = "{number}%".format(
                number = round((sum_measure_data.activation_number_total \
                              / sum_measure_data.volume_total) * 100, 2))
        return sum_measure_data

    @classmethod
    def huang_serviceitem_rate(cls, measure_staff_list):
        """售后服务单产品挂载开通率激活率"""
        product_list = [1, 2]
        for measure_staff in measure_staff_list:

            measure_staff.volume = 0
            measure_staff.conversion_rate = "0%"
            measure_staff.open_number = 0
            measure_staff.open_rate = "0%"
            measure_staff.activation_number = 0
            measure_staff.activation_rate = "0%"

            if measure_staff.report_date:
                report_date = measure_staff.report_date
                report_date_min = datetime.datetime(report_date.year, report_date.month, report_date.day, 0, 0, 0)
                report_date_max = datetime.datetime(report_date.year, report_date.month, report_date.day, 23, 59, 59)
                service_item_qs = cls.search_qs(order__pay_time__gte=report_date_min,
                                                order__pay_time__lte=report_date_max,
                                                service__seller=measure_staff.staff,
                                                equipment_sn__product__id__in=product_list)
                if service_item_qs.count() > 0:
                    for service_item in service_item_qs:
                        if service_item.equipment_sn.sn_status == SnStatus.NORMAL:
                            measure_staff.volume += 1
                            if service_item.dsinfo_status != SnStatusType.RED:
                                measure_staff.open_number += 1
                            if service_item.rebate_status != SnStatusType.RED:
                                measure_staff.activation_number += 1

                    if measure_staff.new_number > 0 and measure_staff.volume > 0:
                        measure_staff.conversion_rate = "{number}%".format(number = round((measure_staff.volume \
                                                                                         / measure_staff.new_number) * 100,
                                                                                        2))
                    if measure_staff.volume > 0 and measure_staff.open_number > 0:
                        measure_staff.open_rate = "{number}%".format(number = round((measure_staff.open_number \
                                                                                   / measure_staff.volume) * 100, 2))
                        measure_staff.activation_rate = "{number}%".format(number = round((measure_staff.activation_number \
                                                                                         / measure_staff.volume) * 100,
                                                                                        2))
        return measure_staff_list

    @classmethod
    def Statistics(cls, measure_staff_mapping, service_item_list):

        for service_item in service_item_list:

            create_time_str = str(service_item.order.pay_time.date())
            temp_item = measure_staff_mapping[create_time_str]
            if service_item.equipment_sn.sn_status == SnStatus.NORMAL:
                temp_item["volume"] += 1
                if service_item.dsinfo_status != SnStatusType.RED:
                    temp_item["open_number"] += 1
                if service_item.rebate_status != SnStatusType.RED:
                    temp_item["activation_number"] += 1

        statistics_list = []

        for measure_staff_mapping_item in measure_staff_mapping:
            temp_measure_item = measure_staff_mapping[measure_staff_mapping_item]
            if temp_measure_item["exhale_number"] > 0 and temp_measure_item["call_number"] > 0:

                temp_measure_item["call_rate"] = "{number}%".format(number = round((temp_measure_item["call_number"] \
                                                                                  / temp_measure_item[
                                                                                      "exhale_number"]) * 100, 2))

            if temp_measure_item["new_number"] > 0 and temp_measure_item["volume"] > 0:

                temp_measure_item["conversion_rate"] = "{number}%".format(number = round((temp_measure_item["volume"] \
                                                                                        / temp_measure_item[
                                                                                            "new_number"]) * 100, 2))
            if temp_measure_item["volume"] > 0 and temp_measure_item["open_number"] > 0:
                temp_measure_item["open_rate"] = "{number}%".format(number = round((temp_measure_item["open_number"] \
                                                                                  / temp_measure_item["volume"]) * 100,
                                                                                 2))
                temp_measure_item["activation_rate"] = "{number}%".format(
                    number = round((temp_measure_item["activation_number"] \
                                  / temp_measure_item["volume"]) * 100, 2))

            temp_measure_item["calculation_date"] = measure_staff_mapping_item

            statistics_list.append(temp_measure_item)

        return statistics_list

    @classmethod
    def get_serviceitem_byequipment(cls, equipment_sn):
        service_item_qs = cls.search_qs(equipment_sn = equipment_sn)
        if service_item_qs.count() > 0:
            return service_item_qs[0]

        return None

    @classmethod
    def update(cls, service_item, **attr):
        service_item.update(**attr)

    @classmethod
    def hung_phonecode_forservice(cls, service_item_list):
        """挂载手机编码"""
        for service_item in service_item_list:
            service_item.phone_code = None
            try:
                code = service_item.customer.mobiledevices.code
                service_item.phone_code = code
            except Exception as e:
                pass
        return service_item_list

    @classmethod
    def hung_devicetype_forservice(cls, service_item_list):
        """ 挂载设备类型"""
        for service_item in service_item_list:
            service_item.device_type = None
            try:
                device_type = service_item.equipment_sn.product.name
                if device_type:
                    service_item.device_type = device_type
            except Exception as e:
                pass
        return service_item_list

    @classmethod
    def get_status(cls, after_sn, er_obj):
        rebate_status = SnStatusType.RED
        rebate_money = EquipmentSn.search(code = after_sn)[0].product.rebate_money
        if rebate_money > 0:
            last_time = add_month(er_obj.bind_time, 2)
            total_money_lastmonth = EquipmentTransaction.sum_money(
                transaction_time__range = (er_obj.bind_time, last_time), code = er_obj)
            if total_money_lastmonth >= rebate_money:
                equipment_rebate_qs = EquipmentRebate.query().filter(code = er_obj,
                                                                     remark__contains = "已达到")
                if equipment_rebate_qs.count() > 0:
                    rebate_status = SnStatusType.TGREEB
                else:
                    rebate_status = SnStatusType.GREEN
            else:
                total_money = EquipmentTransaction.sum_money(code = er_obj)
                if total_money >= rebate_money:
                    rebate_status = SnStatusType.YELLOW

        return rebate_status


    @classmethod
    def del_service_item(cls, service_item):
        if service_item is not None:
            # 20180711 morning--- after discussion, they decide not to remove this event.
            # if service_item.order:
            #   StaffOrderEvent.query(order=service_item.order).delete()
            service_item.delete()
            if ServiceItem.query(service = service_item.service).count() == 0:
                service_item.service.delete()

    @classmethod
    def check_sn_validity(cls, pre_sn, after_sn):
        '''check the sn validity'''
        if not after_sn.isdigit() or pre_sn == after_sn:
            raise BusinessError("请检查SN有效性")
        judge_code = EquipmentIn.search(min_number__lte = after_sn, max_number__gte = after_sn)
        if not judge_code:
            raise BusinessError("要修改的SN不存在!")

    @classmethod
    def get_register_info(cls, pre_sn, after_sn, esn_obj):
        ''' get the pre and after sn's register info '''
        pre_flag = False
        after_flag = False
        pre_er_obj = EquipmentRegister.search(equipment_sn__code = pre_sn)
        after_er_obj = EquipmentRegister.search(device_code = after_sn) if not esn_obj else EquipmentRegister.search(
            equipment_sn__code = after_sn)
        if pre_er_obj:
            pre_flag = True
        if after_er_obj:
            after_flag = True
        return pre_flag, after_flag, pre_er_obj, after_er_obj

    @classmethod
    def pre_sn_register_cut_down(cls, pre_er_obj, pre_flag, pre_sn):
        """the pre sn if registered, then it should be cut down"""
        if not pre_flag:
            print('this will not be show')
            return ''
        pre_er_obj[0].equipment = None
        pre_er_obj[0].equipment_sn = None
        pre_er_obj[0].device_code = pre_sn
        pre_er_obj[0].status = EquipmentStatusState.ABNORMAL
        pre_er_obj[0].save()

    @classmethod
    def after_sn_register_attach(cls, after_sn, after_flag, after_er_obj):
        """ bund after_sn's relationship if it's registered"""
        if not after_flag:
            return ''
        esn_obj = EquipmentSn.search(code = after_sn)[0]
        e_obj = Equipment.search(code = after_sn)[0]
        after_er_obj[0].equipment = e_obj
        after_er_obj[0].equipment_sn = esn_obj
        after_er_obj[0].device_code = after_sn
        after_er_obj[0].status = EquipmentStatusState.NORMAL
        after_er_obj[0].save()

    @classmethod
    def service_item(cls, after_sn, after_flag, after_er_obj):
        """ update server_item info """
        esn_obj = EquipmentSn.search(code = after_sn)[0]
        dsinfo_status = SnStatusType.YELLOW if after_flag else SnStatusType.RED
        rebate_status = SnStatusType.RED
        if after_flag:
            rebate_status = cls.get_status(after_sn, after_er_obj[0])
        si_qs = ServiceItem.search(equipment_sn = esn_obj)
        if si_qs:
            si_obj = si_qs[0]
            si_obj.buyinfo_status = SnStatusType.RED
            si_obj.dsinfo_status = dsinfo_status
            si_obj.rebate_status = rebate_status
            si_obj.sn_status = SnStatusType.GREEN
            si_obj.save()

    @classmethod
    def service_delete(cls, after_sn, after_er_obj):
        if not after_er_obj:
            return ''
        try:
            if Service.search(order = after_er_obj[0].equipment_sn.order)[0].seller == None:
                Equipment.search(code = 'Err' + after_sn).delete()
                esn_temp = EquipmentSn.search(code = 'Err' + after_sn)[0]
                ServiceItem.search(equipment_sn = esn_temp).delete()
                esn_temp.delete()
        except Exception as e:
            print('-------------------->service_delete exception:', e)

    @classmethod
    def process_sn_change(cls, pre_sn, after_sn):
        # step 1: check sn validity
        cls.check_sn_validity(pre_sn, after_sn)
        # step 2: judge the customer in equipment and equipmentsn whther the same
        e_cus = Equipment.search(code = pre_sn)
        en_cus = EquipmentSn.search(code = pre_sn)
        if e_cus[0].customer != en_cus[0].customer:
            # for the time being, this situation does't exist. so just use 'pass' to hold the place ---20180724
            pass
        # step 3: start proccess multi situations
        esn_obj = EquipmentSn.search(code = after_sn)  # whether after_sn is exist
        # get the pre and after sn's register info
        pre_flag, after_flag, pre_er_obj, after_er_obj = cls.get_register_info(pre_sn, after_sn, esn_obj)
        order_obj = EquipmentSn.search(code = pre_sn)[0].order
        try:
            if not esn_obj:
                pre_ee_obj = Equipment.search(code = pre_sn)[0]
                pre_ee_obj.update(code = after_sn, equipment_status = EquipmentStatusState.NORMAL)
                EquipmentSn.search(code = pre_sn).update(code = after_sn, sn_status = EquipmentStatusState.NORMAL)
                li_obj_id = pre_ee_obj.logistics_item_id
                if li_obj_id:
                    li_obj = LogisticsItem.query().filter(id = li_obj_id)[0]
                    esn_list = li_obj.equipment_sn_list.replace(pre_sn, after_sn)
                    li_obj.update(equipment_sn_list = esn_list)
                # if you feel confused, that means you're on the road.
                cls.service_item(after_sn, after_flag, after_er_obj)
                cls.after_sn_register_attach(after_sn, after_flag, after_er_obj)
                cls.pre_sn_register_cut_down(pre_er_obj, pre_flag, pre_sn)
                cls.proccess_returns(pre_sn, after_sn, order_obj)
                return ''
            else:
                ee_after = Equipment.search(code = after_sn)[0]
                ee_pre = Equipment.search(code = pre_sn)[0]
                esn_after = EquipmentSn.search(code = after_sn)[0]
                esn_pre = EquipmentSn.search(code = pre_sn)[0]
                ee_after.update(code = 'Err' + after_sn, equipment_status = EquipmentStatusState.ABNORMAL)
                ee_pre.update(code = after_sn, equipment_status = EquipmentStatusState.NORMAL)
                esn_after.update(code = 'Err' + after_sn, sn_status = EquipmentStatusState.ABNORMAL)
                ServiceItem.search(equipment_sn = esn_after).update(buyinfo_status = SnStatusType.RED,
                                                                  dsinfo_status = SnStatusType.RED,
                                                                  rebate_status = SnStatusType.RED,
                                                                  sn_status = SnStatusType.RED)
                esn_pre.update(code = after_sn, sn_status = EquipmentStatusState.NORMAL)
                # very confused, but ,now it works, why? what's the principle of Django's object?
                try:
                    li_obj_after_id = ee_after.logistics_item_id
                    li_obj_after = LogisticsItem.query().filter(id = li_obj_after_id)[0]
                    li_obj_pre_id = ee_pre.logistics_item_id
                    li_obj_pre = LogisticsItem.query().filter(id = li_obj_pre_id)[0]
                    if li_obj_after:
                        esn_list = li_obj_after.equipment_sn_list.replace(after_sn, 'Err' + after_sn)
                        LogisticsItem.query().filter(id = li_obj_after_id).update(equipment_sn_list = esn_list)
                    if li_obj_pre:
                        esn_list = li_obj_after.equipment_sn_list.replace(pre_sn, after_sn)
                        LogisticsItem.query().filter(id = li_obj_pre_id).update(equipment_sn_list = esn_list)
                except Exception as e:
                    print("modify logisticsitem failed", e)
                cls.after_sn_register_attach(after_sn, after_flag, after_er_obj)
                cls.pre_sn_register_cut_down(pre_er_obj, pre_flag, pre_sn)
                cls.service_item(after_sn, after_flag, after_er_obj)
                cls.service_delete(after_sn, after_er_obj)
                cls.proccess_returns(pre_sn, after_sn, order_obj)
                return "原SN为'{after_sn}'已转为'Err{after_sn}',请及时确认及处理。".format(after_sn = after_sn)
        except Exception as e:
            print('---------------------------------------e', e)
            raise BusinessError("修改失败")

    @classmethod
    def proccess_returns(cls, pre_sn, after_sn, order_obj):
        or_pre_qs = OrderReturns.search(code = pre_sn)
        if or_pre_qs:
            or_pre_qs.update(order = None)
            StaffReturnsEvent.search(order_returns = or_pre_qs[0]).update(staff = None, server = None, department = None)
        or_after_qs = OrderReturns.search(code = after_sn)
        esn_after_qs = EquipmentSn.search(code = after_sn)
        er_after_qs = EquipmentRegister.search(device_code = after_sn)
        update_info = {'customer': None, 'logistics_item': None, 'order': None}
        if or_after_qs:
            s = Service.search(order = esn_after_qs[0].order)
            staff = None
            server = None
            department = None
            if s:
                staff = s[0].seller
                server = s[0].server
                aa_obj = AuthAccess.search(staff = staff, access_type = 'department')
                if aa_obj:
                    department = Department.query(id = aa_obj[0].access_id)
                    if department:
                        department = department[0]
            StaffReturnsEvent.search(order_returns = or_after_qs[0]).update(staff = staff, server = server,
                                                                          department = department)
            or_after_qs[0].order = order_obj
            or_after_qs[0].save()
            if er_after_qs:
                esn_after_qs[0].update(sn_status = SnStatus.RGOODS)
                esn_after_qs[0].equipment.update(**update_info)
            if not er_after_qs:
                service_item_qs = ServiceItem.query(equipment_sn = after_sn)
                service_item = None
                if service_item_qs.count() > 0:
                    service_item = service_item_qs[0]
                cls.del_service_item(service_item)
                esn_after_qs[0].equipment.delete()
                esn_after_qs[0].delete()
