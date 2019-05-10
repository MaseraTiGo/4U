# coding=UTF-8

'''
Created on 2016年7月22日

@author: Administrator
'''

from django.db.models import *
from model.models import MeasureStaff
from model.models import Staff
from model.store.model_department import Department
from model.store.model_equipment import EquipmentStatusType
from model.store.model_equipment_sn import SnStatusType, SnStatus
from model.store.model_merchant_equipment import MerchantEquipment
from model.store.model_order_event import StaffOrderEvent
from model.store.model_service import ServiceItem

from tuoen.abs.middleware.department import department_middleware
from tuoen.sys.core.exception.business_error import BusinessError
from tuoen.sys.utils.common.dictwrapper import DictWrapper
from tuoen.sys.utils.common.split_page import Splitor


class MeasureStaffHelper(object):

    @classmethod
    def generate(cls, **measure_staff_info):
        """创建员工绩效"""

        measure_staff = MeasureStaff.create(**measure_staff_info)
        if measure_staff is None:
            raise BusinessError("员工绩效添加失败")

        return measure_staff

    @classmethod
    def search(cls, current_page, measure_staff_qs):
        """查询员工绩效列表"""

        measure_staff_qs = measure_staff_qs.order_by("-report_date")
        return Splitor(current_page, measure_staff_qs)

    # retB = list(set(listA).intersection(set(listB)))
    @classmethod
    def search_qs(cls, **search_info):
        if 'department_id' in search_info:
            department_id = search_info.pop('department_id')
            department_ids = department_middleware.get_all_children_ids(department_id)
            department_ids.append(department_id)

            search_info.update({"department_id__in": department_ids})
        if 'cur_user' in search_info:
            user_pro = search_info.pop('cur_user')
            if not user_pro._is_admin:
                if "staff_id__in" in search_info:
                    search_info.update({"staff_id__in": list(
                        set(search_info["staff_id__in"]).intersection(set(user_pro._staff_id_list)))})
                else:
                    search_info.update({"staff_id__in": user_pro._staff_id_list})
        if "begin_time" in search_info:
            begin_time = search_info.pop("begin_time")
            search_info.update({"report_date__gte": begin_time})
        if "end_time" in search_info:
            end_time = search_info.pop("end_time")
            search_info.update({"report_date__lte": end_time})
        measure_staff_qs = MeasureStaff.search(**search_info)
        return measure_staff_qs

    @classmethod
    def check_repeat(cls, measure_staff=None, **check_info):
        measure_staff_qs = cls.search_qs(**check_info)
        if measure_staff is not None:
            measure_staff_qs = measure_staff_qs.filter(~Q(id=measure_staff.id))
        if measure_staff_qs.count() > 0:
            raise BusinessError("请不要添加重复绩效")
        return True

    @classmethod
    def search_by_month(cls, **search_info):

        measure_staff_qs = MeasureStaff.search(**search_info)

        return measure_staff_qs

    @classmethod
    def get(cls, measure_staff_id):
        """获取员工绩效详情"""

        measure_staff = MeasureStaff.get_byid(measure_staff_id)
        if measure_staff is None:
            raise BusinessError("员工绩效不存在")
        return measure_staff

    @classmethod
    def update(cls, measure_staff, **attrs):
        """编辑员工绩效"""

        measure_staff.update(**attrs)
        return True

    @classmethod
    def remove(cls, measure_staff_id):
        """移除员工绩效"""

        measure_staff = cls.get(measure_staff_id)
        measure_staff.delete()

        return True

    @classmethod
    def summing_new(cls, **search_info):
        """计算统计"""
        sum_data = DictWrapper({})
        measure_staff_qs = cls.search_qs(**search_info)
        measure_staff_result = measure_staff_qs.aggregate(sum_new_number=Sum('new_number'), \
                                                          sum_exhale_number=Sum('exhale_number'), \
                                                          sum_call_number=Sum('call_number'), \
                                                          sum_wechat_number=Sum('wechat_number'))
        sum_data.new_number = measure_staff_result["sum_new_number"] if measure_staff_result["sum_new_number"] else 0
        sum_data.exhale_number = measure_staff_result["sum_exhale_number"] if measure_staff_result[
            "sum_exhale_number"] else 0
        sum_data.call_number = measure_staff_result["sum_call_number"] if measure_staff_result["sum_call_number"] else 0
        sum_data.wechat_number = measure_staff_result["sum_wechat_number"] if measure_staff_result[
            "sum_wechat_number"] else 0
        sum_data.call_rate = "0%"

        if sum_data.exhale_number > 0:
            sum_data.call_rate = "{rate}%".format(
                rate=str(round((sum_data.call_number / sum_data.exhale_number * 100), 2)))

        return sum_data

    @classmethod
    def staff_sum_list(cls, current_page, is_split=True, **search_info):
        """calculate single staff's measure in one month"""
        date_min = search_info['begin_time']
        date_max = search_info['end_time']
        flag = False
        if 'new_protect' in search_info:
            flag = True
            new_protect = search_info.pop('new_protect')
        measure_staff_qs = cls.search_qs(**search_info)
        iter_obj = MeasureStaff.get_annotate_data(measure_staff_qs)
        staff_list = []
        for item in iter_obj:
            staff_data = DictWrapper({})
            staff = Staff.search(id=item[0])[0]
            staff_data.staff_id = item[0]
            staff_data.staff = staff
            staff_data.staff_name = staff.name
            staff_data.department = Department.search(id=item[1])[0].name
            staff_data.new_number = item[2]
            staff_data.exhale_number = item[3]
            staff_data.call_number = item[4]

            staff_data.call_rate = "0%"
            if item[3] > 0:
                staff_data.call_rate = str(round((item[4] / item[3] * 100), 2)) + '%'
            staff_data.wechat_number = item[5]
            cls.is_protect(staff_data, date_min, date_max)
            cls.hung_serviceitem_rate(staff, date_min, date_max, staff_data)
            cls.hung_ysb_measure_data(staff_data, date_min, date_max)
            staff_list.append(staff_data)
        if flag:
            staff_list = [staff for staff in staff_list if staff.new_protect == new_protect]
        if is_split:
            return Splitor(current_page, staff_list)
        else:
            return staff_list

    @classmethod
    def is_protect(cls, staff_obj, date_min, date_max):
        """judge whether this staff is been protected"""
        staff_obj.new_protect = False
        soe_qs = StaffOrderEvent.search(**{'order__pay_time__gte': date_min,
                                           'order__pay_time__lte': date_max,
                                           'is_count': 'countout'})
        if soe_qs:
            staff_obj.new_protect = True

    @classmethod
    def hung_serviceitem_rate(cls, staff, date_min, date_max, staff_data):
        """single staff hung the rate about opened and activation"""
        staff_data.volume = 0
        staff_data.conversion_rate = "0%"
        staff_data.open_number = 0
        staff_data.open_rate = "0%"
        staff_data.activation_number = 0
        staff_data.activation_rate = "0%"
        staff_data.new_protect = False
        product_list = [1, 2]
        service_item_qs = ServiceItem.search(order__pay_time__gte=date_min,
                                             order__pay_time__lte=date_max,
                                             service__seller=staff,
                                             equipment_sn__product__id__in=product_list)
        if service_item_qs.count() > 0:
            for service_item in service_item_qs:
                if service_item.equipment_sn.sn_status == SnStatus.NORMAL:
                    staff_data.volume += 1
                    if service_item.dsinfo_status != SnStatusType.RED:
                        staff_data.open_number += 1
                    if service_item.rebate_status != SnStatusType.RED:
                        staff_data.activation_number += 1

            if staff_data.new_number > 0 and staff_data.volume > 0:
                staff_data.conversion_rate = "{number}%".format(number=round((staff_data.volume
                                                                              / staff_data.new_number) * 100,
                                                                             2))
            if staff_data.volume > 0 and staff_data.open_number > 0:
                staff_data.open_rate = "{number}%".format(number=round((staff_data.open_number
                                                                        / staff_data.volume) * 100, 2))
                staff_data.activation_rate = "{number}%".format(number=round((staff_data.activation_number
                                                                              / staff_data.volume) * 100,
                                                                             2))

    @classmethod
    def total_calculate(cls, **search_info):
        """get all the data that all staff's data count in"""
        sum_data = DictWrapper({})
        measure_staff_qs = cls.search_qs(**search_info)
        measure_staff_result = measure_staff_qs.aggregate(sum_new_number=Sum('new_number'),
                                                          sum_exhale_number=Sum('exhale_number'),
                                                          sum_call_number=Sum('call_number'),
                                                          sum_wechat_number=Sum('wechat_number'))
        sum_data.new_number = measure_staff_result["sum_new_number"] if measure_staff_result["sum_new_number"] else 0
        sum_data.exhale_number = measure_staff_result["sum_exhale_number"] if measure_staff_result[
            "sum_exhale_number"] else 0
        sum_data.call_number = measure_staff_result["sum_call_number"] if measure_staff_result["sum_call_number"] else 0
        sum_data.wechat_number = measure_staff_result["sum_wechat_number"] if measure_staff_result[
            "sum_wechat_number"] else 0
        sum_data.call_rate = "0%"

        if sum_data.exhale_number > 0:
            sum_data.call_rate = "{rate}%".format(
                rate=str(round((sum_data.call_number / sum_data.exhale_number * 100), 2)))

        return sum_data

    @classmethod
    def calculate_rate_common(cls, new_number, volume, open_number, activation_number):
        """calculate rate that every product can use"""
        conversion_rate = ''
        open_rate = ''
        activation_rate = ''
        if new_number > 0 and volume > 0:
            conversion_rate = "{number}%".format(number=round((volume
                                                               / new_number) * 100,
                                                              2))
        if volume > 0 and open_number > 0:
            open_rate = "{number}%".format(number=round((open_number
                                                         / volume) * 100, 2))
            activation_rate = "{number}%".format(number=round((activation_number
                                                               / volume) * 100,
                                                              2))
        return conversion_rate, open_rate, activation_rate

    @classmethod
    def hung_total_rate(cls, sum_data, **search_info):
        """statistics, this page's data use this function """
        product_list = [1, 2]
        sum_measure_data = DictWrapper({})
        sum_measure_data.volume_total = 0
        sum_measure_data.open_number_total = 0
        sum_measure_data.activation_number_total = 0
        sum_measure_data.conversion_rate_total = "0%"
        sum_measure_data.open_rate_total = "0%"
        sum_measure_data.activation_rate_total = "0%"
        service_item_qs = cls.get_service_item_qs(product_list, **search_info)
        sum_measure_data.volume_total = \
            service_item_qs.filter(equipment_sn__sn_status=SnStatus.NORMAL).aggregate(total_num=Count('id'))[
                "total_num"]

        sum_measure_data.open_number_total = service_item_qs.filter(equipment_sn__sn_status=SnStatus.NORMAL).filter(
            ~Q(dsinfo_status=EquipmentStatusType.RED)).aggregate(total_num=Count('id'))["total_num"]

        sum_measure_data.activation_number_total = \
            service_item_qs.filter(equipment_sn__sn_status=SnStatus.NORMAL).filter(
                ~Q(rebate_status=SnStatusType.RED)).aggregate(total_num=Count('id'))["total_num"]

        conversion_rate, open_rate, activation_rate = cls.calculate_rate_common(sum_data.new_number,
                                                                                sum_measure_data.volume_total,
                                                                                sum_measure_data.open_number_total,
                                                                                sum_measure_data.activation_number_total)
        sum_measure_data.conversion_rate_total = conversion_rate
        sum_measure_data.open_rate_total = open_rate
        sum_measure_data.activation_rate_total = activation_rate
        return sum_measure_data

    @classmethod
    def ysb_calculate_rate(cls, service_item_qs, new_number):
        """calculate ysb's rate"""
        ds_sn_list = []
        rebate_sn_list = []
        ysb_volume = 0
        if service_item_qs.count() > 0:
            for service_item in service_item_qs:
                if service_item.equipment_sn.sn_status == SnStatus.NORMAL:
                    ysb_volume += 1
                    if service_item.dsinfo_status != SnStatusType.RED:
                        ds_sn_list.append(service_item.equipment_sn)
                    if service_item.rebate_status != SnStatusType.RED:
                        rebate_sn_list.append(service_item.equipment_sn)

        me_search_info = {'equipment_sn__in': rebate_sn_list,
                          'merchant__is_activation': 1}
        me_qs = MerchantEquipment.search(**me_search_info)
        ysb_activation_number = len(set([me.merchant for me in me_qs]))

        me_search_info = {'equipment_sn__in': ds_sn_list}
        me_qs = MerchantEquipment.search(**me_search_info)
        ysb_open_number = len(set([me.merchant for me in me_qs]))
        conversion_rate, open_rate, activation_rate = cls.calculate_rate_common(new_number,
                                                                                ysb_volume,
                                                                                ysb_open_number,
                                                                                ysb_activation_number)

        ysb_conversion_rate = conversion_rate
        ysb_open_rate = open_rate
        ysb_activation_rate = activation_rate
        return ysb_conversion_rate, ysb_open_rate, ysb_activation_rate

    @classmethod
    def hung_ysb_measure_data(cls, staff_obj, date_min=0, date_max=0):
        """single staff hung the ysb rate"""
        product_list = [3]
        if isinstance(staff_obj, Staff):
            staff = staff_obj
        else:
            staff = staff_obj.staff
        staff_obj.ysb_volume = 0
        staff_obj.ysb_conversion_rate = "0%"
        staff_obj.ysb_open_number = 0
        staff_obj.ysb_open_rate = "0%"
        staff_obj.ysb_activation_number = 0
        staff_obj.ysb_activation_rate = "0%"
        staff_obj.new_protect = False
        if date_min == 0:
            service_item_qs = ServiceItem.search(service__seller=staff,
                                                 equipment_sn__product__id__in=product_list)
        else:
            service_item_qs = ServiceItem.search(order__pay_time__gte=date_min,
                                                 order__pay_time__lte=date_max,
                                                 service__seller=staff,
                                                 equipment_sn__product__id__in=product_list)

        staff_obj.ysb_conversion_rate, staff_obj.ysb_open_rate, staff_obj.ysb_activation_rate = \
            cls.ysb_calculate_rate(service_item_qs, staff_obj.new_number)

    @classmethod
    def get_service_item_qs(cls, product_list, **search_info):
        """according to the search info , get the service item query set"""
        soe_qs = StaffOrderEvent.search(**{'order__pay_time__gte': search_info['begin_time'],
                                           'order__pay_time__lte': search_info['end_time'],
                                           'is_count': 'countin'})
        effective_order_list = [soe.order for soe in soe_qs]
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
            search_info.update({"order__pay_time__gte": begin_time})

        if "end_time" in search_info:
            end_time = search_info.pop("end_time")
            search_info.update({"order__pay_time__lte": end_time})

        if "staff" in search_info:
            staff = search_info.pop("staff")
            search_info.update({"service__seller": staff})
        search_info.update({'equipment_sn__product__id__in': product_list})
        service_item_qs = ServiceItem.search(**search_info)
        service_item_qs = service_item_qs.filter(order__in=effective_order_list)
        return service_item_qs

    @classmethod
    def hung_ysb_total_rate(cls, sum_data, **search_info):
        """hung the ysb rate to the statistics data"""
        product_list = [3]
        ysb_sum_measure_data = DictWrapper({})
        ysb_sum_measure_data.volume_total = 0
        ysb_sum_measure_data.open_number_total = 0
        ysb_sum_measure_data.activation_number_total = 0
        ysb_sum_measure_data.conversion_rate_total = "0%"
        ysb_sum_measure_data.open_rate_total = "0%"
        ysb_sum_measure_data.activation_rate_total = "0%"
        service_item_qs = cls.get_service_item_qs(product_list, **search_info)
        ysb_sum_measure_data.volume_total = \
            service_item_qs.filter(equipment_sn__sn_status=SnStatus.NORMAL).aggregate(total_num=Count('id'))[
                "total_num"]

        ysb_sum_measure_data.conversion_rate_total, ysb_sum_measure_data.open_rate_total, \
            ysb_sum_measure_data.activation_rate_total = cls.ysb_calculate_rate(
                service_item_qs, sum_data.new_number)
        return ysb_sum_measure_data
