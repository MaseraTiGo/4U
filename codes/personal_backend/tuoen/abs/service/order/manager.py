# coding=UTF-8

'''
Created on 2016年7月22日

@author: Administrator
'''

import hashlib
import datetime
import json
from io import StringIO
import random
from tuoen.sys.core.exception.business_error import BusinessError
from tuoen.sys.utils.common.split_page import Splitor

from tuoen.abs.middleware.journal import JournalMiddleware
from tuoen.abs.middleware.department import department_middleware
from model.models import StaffOrderEvent, Order, OrderItem, \
Equipment, Service, ServiceItem, EquipmentStatusState, EquipmentRegister, EquipmentSn
from model.store.model_orderreturns import OrderReturns, ReturnsNum
from model.store.model_journal import JournalTypes, OperationTypes
from model.models import EquipmentSn, SnStatus, SnStatusType

from model.store.model_measure_staff import MeasureStaff

from model.store.model_returnsevent import StaffReturnsEvent
from model.store.model_logistics import LogisticsItem
from model.store.model_equipment_in import EquipmentIn
from model.store.model_product import Product, ProductModel
from model.store.model_auth_access import AuthAccess
from model.store.model_department import Department
from model.store.model_shop import Goods
from model.store.model_mobilephone import MobileMaintain
from model.store.model_repenishment import Replenishment, ReplenishmentItem, Restatus
from model.store.model_repenishment import ReplenishmentEvent, ReplenishmentNum
from model.store.model_order_event import StaffOrderEvent

class StaffOrderEventServer(object):

    @classmethod
    def search(cls, current_page, **search_info):
        """查询事件列表"""

        staff_orser_event_qs = StaffOrderEvent.query(**search_info)

        staff_orser_event_qs = staff_orser_event_qs.order_by("-create_time")
        return Splitor(current_page, staff_orser_event_qs)


    @classmethod
    def get_event_byorder(cls, order):
        """通过订单查询事件"""

        try:
            return StaffOrderEvent.query(order = order)[0]
        except:
            return None

    @classmethod
    def get_event_bystaff(cls, staff_list):
        """通过员工查询事件"""

        try:
            return StaffOrderEvent.search(staff__in = staff_list)
        except:
            return []

    @classmethod
    def hung_staff_fororders(cls, order_list):
        """批量订单挂载员工"""
        order_mapping = {}
        for order in order_list:
            order_mapping[order.id] = order
            order_mapping[order.id].staff = None
            order_mapping[order.id].department = None
        order_event_list = StaffOrderEvent.search(order_id__in = order_mapping.keys())
        for order_event in order_event_list:
            if order_event.order.id in order_mapping:
                order_mapping[order_event.order.id].staff = order_event.staff
                order_mapping[order_event.order.id].department = order_event.department

        return order_list

    @classmethod
    def get_orders_bydepartmentids(cls, department_ids):
        """通过部门id查询订单id"""
        order_ids = []
        staff_order_event_qs = StaffOrderEvent.query().values('order_id').filter(department_id__in = department_ids)
        for staff_order_event in staff_order_event_qs:
            order_ids.append(staff_order_event["order_id"])

        return order_ids

    @classmethod
    def hung_department_byserviceitem(cls, service_item_list):
        """通过售后服务单详情挂在部门"""
        order_id = []
        staff_order_event_mapping = {}
        for servict_item in service_item_list:
            order_id.append(servict_item.order_id)

        staff_order_event_qs = StaffOrderEvent.search(order_id__in = order_id)

        for staff_order_event in staff_order_event_qs:
            staff_order_event_mapping[staff_order_event.order_id] = staff_order_event

        for servict_item in service_item_list:
            if servict_item.order_id in staff_order_event_mapping:
                servict_item.department = staff_order_event_mapping[servict_item.order_id].department
            else:
                servict_item.department = None

        return service_item_list

class OrderServer(object):
    @classmethod
    def get(cls, order_id):
        """获取渠道详情"""

        order = Order.get_byid(order_id)
        if order is None:
            raise BusinessError("订单不存在")
        return order

    @classmethod
    def search_qs(cls, **search_info):
        soe_search_info = {}
        if "cur_user" in search_info:
            user_pro = search_info.pop('cur_user')
        if "begin_time" in search_info:
            begin_time = search_info.pop("begin_time")
            search_info.update({"pay_time__gte":begin_time})
        if "end_time" in search_info:
            end_time = search_info.pop("end_time")
            search_info.update({"pay_time__lte":end_time})
        if "department" in search_info:
            dept_id = search_info.pop("department")
            dept_list = department_middleware.get_all_children_ids(dept_id)
            dept_list.append(dept_id)
            soe_search_info.update({"department__id__in": dept_list})
        if "server" in search_info:
            server_id = search_info.pop("server")
            soe_search_info.update({"staff__id": server_id})
        if soe_search_info:
            order_ids = [soe.order.id for soe in StaffOrderEvent.search(**soe_search_info)]
            search_info.update({"id__in": order_ids})
        order_qs = Order.search(**search_info)
        return order_qs

    @classmethod
    def search(cls, current_page, **search_info):
        """查询所有订单列表"""
        user_pro = search_info['cur_user']
        order_qs = cls.search_qs(**search_info)
        if not user_pro._is_show_sub:
            event_id = StaffOrderEvent.query(staff_id__exact = user_pro._cur_user_id)[0].id
            order_qs = order_qs.filter(id__exact = event_id)
        order_qs = order_qs.order_by("-create_time")
        return Splitor(current_page, order_qs)

    @classmethod
    def search_by_paytime(cls, search_time = None):
        """根据月份查询订单"""

        if search_time is None:
            current_time = datetime.datetime.now()
        else:
            current_time = search_time

        cur_date_first = datetime.datetime(current_time.year, current_time.month, 1)
        cur_date_last = datetime.datetime(current_time.year, current_time.month + 1, 1, 23, 59, 59) - datetime.timedelta(1)

        order_qs = cls.search_qs(begin_time = cur_date_first, end_time = cur_date_last, id__in = order_ids)

        return order_qs

    @classmethod
    def get_order_byevent(cls, event_list):
        """根据事件列表查询订单列表"""
        order_list = []
        for event in event_list:
            OrderItemServer.hung_item_fororder(event.order)
            order_list.append(event.order)

        return order_list

    @classmethod
    def get_order_byservice(cls, service_list):
        """根据服务单列表查询订单列表"""
        order_list = []
        for service in service_list:
            order_list.append(service.order)

        return order_list

    @classmethod
    def hung_shop_forservice(cls, service_item_list):
        """根据服务单详情挂载店铺"""
        order_ids = []
        for service_item in service_item_list:
            if service_item.service and service_item.service.order_id:
                order_ids.append(service_item.service.order_id)

        order_mapping = {}
        if len(order_ids) > 0:
            order_mapping = {order.id:order for order in \
                            Order.search(id__in = order_ids)}

        for service_item in service_item_list:
            service_item.shop = None
            if service_item.service and service_item.service.order_id:
                order = order_mapping.get(service_item.service.order_id, None)
                if order is not None and order.shop:
                    service_item.shop = order.shop

        return service_item_list

    @classmethod
    def transfer_order_tostaff(cls, order, staff, auth_user, department):
        """将一笔订单移交给一个客服或部门"""

        pre_staff = None

        order_event_qs = StaffOrderEvent.query(order = order)
        if order_event_qs.count() > 0:
            order_event = order_event_qs[0]
            pre_staff = order_event.staff
            order_event.update(staff = staff, department = department)
        else:
            StaffOrderEvent.create(staff = staff, order = order, department = department)

        service_qs = Service.search(order = order)
        if service_qs.count() > 0:
            service = service_qs[0]
            service.update(seller = staff, server = staff)

        # 判断迁移后的员工在这个时间点是否存在绩效
        pay_time = order.pay_time
        buy_data = datetime.datetime(pay_time.year, pay_time.month, pay_time.day)
        # --- performace
        measure_staff_qs = MeasureStaff.search(staff = staff, report_date = buy_data)
        if measure_staff_qs.count() == 0:
            MeasureStaff.create(staff = staff, report_date = buy_data, department = department)

        record_detail = "{who} 在 {datetime} 将 {pre} 的订单号为 {order_id} 的订单移交给了员工 {after} 移交到了部门 {department}".format(who = auth_user.name, \
                                                                      datetime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), \
                                                                      pre = pre_staff.name if pre_staff else "系统", \
                                                                      order_id = order.order_sn, after = staff.name, \
                                                                      department = department.name)

        remark = "转移订单"
        JournalMiddleware.register(auth_user, OperationTypes.STAFF, pre_staff, \
                       OperationTypes.STAFF, JournalTypes.UPDATE, record_detail, remark)

    @classmethod
    def hung_order_returns(cls, order):
        order.returns = []
        ors_qs = OrderReturns.search(order = order)
        for ors in ors_qs:
            ors.amount = ''
            ors.product = ''
            ors.status = '已退货'
            ors.quantity = 1
            product_model = EquipmentIn.search(min_number__lte = ors.code).filter(max_number__gte = ors.code)[0].product_model
            oi = OrderItem.search(order = ors.order)
            if oi:
                price = oi[0].price / 100
            ors.product = product_model
            ors.amount = price
        order.returns = ors_qs

    @classmethod
    def hung_order_replenishment(cls, order):
        order.replenishment = []
        ri_qs = ReplenishmentItem.search(replenishment__order = order)
        for ri in ri_qs:
            ri.rep_num = ri.replenishment.replenishment_num
            ri.rep_create_time = ri.replenishment.create_time
            ri.rep_status = ri.status
            ri.rep_product = ri.goods.name
            ri.rep_sn = ri.code.code
            ri.rep_quantity = ri.replenishment.quantity
            ri.rep_remark = ri.remark
        order.replenishment = ri_qs


class OrderItemServer(object):

    @classmethod
    def search(cls, **search_info):
        """查询订单详情列表"""

        order_item_qs = OrderItem.query(**search_info)

        return order_item_qs

    @classmethod
    def hung_item_fororder(cls, order):
        """订单挂载订单详情"""
        order_item_qs = cls.search(order = order)
        for oi in order_item_qs:
            li_obj_list = [li.id for li in LogisticsItem.query().filter(order_item = oi)]
            e_qs = Equipment.search(logistics_item_id__in = li_obj_list,
                                    equipment_status = EquipmentStatusState.NORMAL)
            code_list = [e.code for e in e_qs]
            oi.sn_list = code_list

        order.items = order_item_qs
        return order

    @classmethod
    def hung_item_fororders(cls, order_list):
        """批量订单挂载订单详情"""
        order_mapping = {}
        for order in order_list:
            order_mapping[order.id] = order
            order_mapping[order.id].items = []
        order_item_list = OrderItem.search(order_id__in = order_mapping.keys())
        for order_item in order_item_list:
            if order_item.order.id in order_mapping:
                order_mapping[order_item.order.id].items.append(order_item)

        return order_list

    @classmethod
    def get(cls, order_item_id):
        """订单详情详情"""
        order_item = OrderItem.get_byid(order_item_id)
        if order_item is None:
            raise BusinessError("订单详情不存在")

        return order_item

class OrderReturnsServer(object):
    @classmethod
    def get(cls, order_id):
        """获取渠道详情"""
        o_obj = Order.search(id = order_id)
        ors_qs = OrderReturns.search(order = o_obj)
        if not ors_qs:
            raise BusinessError("订单不存在")
        return ors_qs

    @classmethod
    def search_qs(cls, **search_info):
        flag = False
        user_pro = search_info.pop('cur_user')
        search_info.update({'staff__id__in': user_pro._staff_id_list})
        if 'seller' in search_info:
            seller = search_info.pop('seller')
            search_info.update({'staff__id': seller})
        if 'department' in search_info:
            dept_id = search_info.pop("department")
            dept_list = department_middleware.get_all_children_ids(dept_id)
            dept_list.append(dept_id)
            search_info.update({"department__id__in": dept_list})
        if 'order_sn' in search_info:
            order_sn = search_info.pop('order_sn')
            search_info.update({'order_returns__order__order_sn': order_sn})
        if "create_time_start" in search_info:
            begin_time = search_info.pop("create_time_start")
            search_info.update({"order_returns__create_time__gte": begin_time})
        if "create_time_end" in search_info:
            end_time = search_info.pop("create_time_end")
            search_info.update({"order_returns__create_time__lte": end_time})
        if "consignee" in search_info:
            consignee = search_info.pop('consignee')
            search_info.update({'order_returns__order__consignee': consignee})
        if "phone" in search_info:
            phone = search_info.pop('phone')
            search_info.update({'order_returns__order__phone': phone})
        if "shop" in search_info:
            shop = search_info.pop('shop')
            search_info.update({'order_returns__order__shop__name': shop})
        if "remark" in search_info:
            remark = search_info.pop('remark')
            search_info.update({'order_returns__order__remark': remark})
        if "code" in search_info:
            code = search_info.pop('code')
            search_info.update({'order_returns__code': code})
        if "returns_num" in search_info:
            returns_num = search_info.pop('returns_num')
            search_info.update({'order_returns__returns_num': returns_num})
        sre_qs = StaffReturnsEvent.search(**search_info)
        sre_qs = sre_qs.order_by("-create_time")
        order_returns_qs = [sre.order_returns for sre in sre_qs]
        return order_returns_qs

    @classmethod
    def search(cls, current_page, **search_info):
        """查询所有订单列表"""
        order_returns_qs = cls.search_qs(**search_info)
        return Splitor(current_page, order_returns_qs)

    @classmethod
    def handle_device_code(cls, device_code):

        device_code = device_code.strip()
        device_code_len = len(device_code)
        if device_code_len == 19:
            device_code = device_code[4:]
        elif device_code_len == 20:
            device_code = device_code[4:-1]
        else:
            return False, 0

        return True, device_code

    @classmethod
    def add(cls, **returns_info):
        ors = None
        department = None
        staff = None
        server = None
        remark = ''
        buyinfo_status = ''
        dsinfo_status = ''
        rebate_status = ''
        sn_status = ''
        returns_num = ReturnsNum().returns_num
        if 'remark' in returns_info:
            remark = returns_info.pop('remark')
        if 'code' in returns_info:
            code_list = returns_info.pop('code').split('.')
        for code in code_list:
            flag, code = cls.handle_device_code(code)
            if not flag:
                raise  BusinessError("设备编码异常")
            esn_obj = EquipmentSn.query(code = code)
            e_obj = Equipment.query(code = code)
            if esn_obj:
                order = esn_obj[0].order
                last_cal_time = esn_obj[0].last_cal_time
                total_amount = esn_obj[0].total_amount
                si_obj = ServiceItem.search(order = order)
                if si_obj:
                    buyinfo_status = si_obj[0].buyinfo_status
                    dsinfo_status = si_obj[0].dsinfo_status
                    rebate_status = si_obj[0].rebate_status
                    sn_status = si_obj[0].sn_status
                ors = OrderReturns.create(code = code, order = order, remark = remark, \
                                          buyinfo_status = buyinfo_status, dsinfo_status = dsinfo_status, \
                                          rebate_status = rebate_status, sn_status = sn_status, \
                                          last_cal_time = last_cal_time, total_amount = total_amount, \
                                          returns_num = returns_num)
                s = Service.search(order = order)
                if s:
                    staff = s[0].seller
                    server = s[0].server
                    aa_obj = AuthAccess.search(staff = staff, access_type = 'department')
                    if aa_obj:
                        department = Department.query(id = aa_obj[0].access_id)
                        if department:
                            department = department[0]
                StaffReturnsEvent.create(staff = staff, server = server, order_returns = ors, department = department)
            remove_info = {'code': code}
            cls.remove(**remove_info)
        return ors

    @classmethod
    def update(cls, **update_info):
        order_id = update_info.pop('id')
        order = Order.query(id = order_id)
        if order:
            update_info.update({'order': order[0]})
            OrderReturns().update(**update_info)

    @classmethod
    def remove(cls, **remove_info):
        staff = None
        server = None
        department = None
        returns_num = ReturnsNum().returns_num
        update_info = {'customer': None, 'logistics_item': None, 'order': None}
        code = remove_info.pop('code')
        equipmentsn_qs = EquipmentSn.query(code = code)
        if equipmentsn_qs.count() > 0:
            eqsn = equipmentsn_qs[0]

            service_item_qs = ServiceItem.query(equipment_sn = eqsn)
            service_item = None
            if service_item_qs.count() > 0:
                service_item = service_item_qs[0]


            order_returns_qs = OrderReturns.query().filter(code = eqsn.code)
            if order_returns_qs.count() == 0:
                ors = OrderReturns.create(code = eqsn.code, order = eqsn.order, returns_num = returns_num, \
                                          buyinfo_status = service_item.buyinfo_status if service_item else SnStatusType.RED, \
                                          dsinfo_status = service_item.dsinfo_status if service_item else SnStatusType.RED, \
                                          rebate_status = service_item.rebate_status if service_item else SnStatusType.RED, \
                                          sn_status = service_item.sn_status if service_item else SnStatusType.RED)
                s = Service.search(order = eqsn.order)
                if s:
                    staff = s[0].seller
                    server = s[0].server
                    aa_obj = AuthAccess.search(staff = staff, access_type = 'department')
                    if aa_obj:
                        department = Department.query(id = aa_obj[0].access_id)
                        if department:
                            department = department[0]
                StaffReturnsEvent.create(staff = staff, server = server, order_returns = ors, department = department)
            equipment_register_qs = EquipmentRegister.query(equipment_sn = eqsn)
            if equipment_register_qs.count() > 0:
                eqsn.update(sn_status = SnStatus.RGOODS)
                eqsn.equipment.update(**update_info)
            else:
                cls.del_service_item(service_item)
                eqsn.equipment.delete()
                eqsn.delete()
        else:
            raise BusinessError("设备编码错误")

        return True

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
    def change(cls, **change_info):
        code = change_info.pop('code')
        flag = change_info.pop('flag')
        equipmentsn_qs = EquipmentSn.query(code = code)
        if equipmentsn_qs.count() > 0:
            equipmentsn = equipmentsn_qs[0]
            equipmentsn.update(sn_status = flag)
            equipmentsn.equipment.update(equipment_status = flag)
        else:
            raise BusinessError("该设备不存在")

    @classmethod
    def recover(cls, **recover_info):
        code = recover_info.pop('code')
        eq = Equipment.search(code = code)
        if eq:
            if eq[0].customer:
                raise BusinessError("SN已绑定新客户，不能恢复！")
        ors_obj = OrderReturns.search(code = code)[0]
        ors_event = StaffReturnsEvent.search(order_returns = ors_obj)[0]
        try:
            # get logicticsItem obj
            li_obj = LogisticsItem.query().filter(equipment_sn_list__contains = code).order_by("-create_time")[0]
            # Create Service
            equipment_sn_qs = EquipmentSn.search(code = code)
            if equipment_sn_qs:
                equipment_sn = equipment_sn_qs[0]
                equipment_sn.update(sn_status = SnStatus.NORMAL)
                e_obj = equipment_sn.equipment.update(last_cal_time = ors_obj.last_cal_time, total_amount = ors_obj.total_amount, \
                                                      customer = ors_obj.order.customer, logistics_item = li_obj, order = ors_obj.order, \
                                                      equipment_status = SnStatus.NORMAL)
            else:
                # get product_model obj & product_obj
                product_model = EquipmentIn.search(min_number__lte = code).filter(max_number__gte = code)[0].product_model
                pm_obj = ProductModel.search(name = product_model)[0]

                service_qs = Service.search(order = ors_obj.order)
                if service_qs:
                    s_obj = service_qs[0]
                else:
                    s_obj = Service.create(customer = ors_obj.order.customer, order = ors_obj.order, seller = ors_event.staff, \
                               server = ors_event.server, end_time = datetime.datetime.now() + datetime.timedelta(days = 5))
                # create equipment
                e_obj = Equipment.create(code = code, last_cal_time = ors_obj.last_cal_time, total_amount = ors_obj.total_amount, \
                                         customer = ors_obj.order.customer, logistics_item = li_obj, order = ors_obj.order, \
                                         product = pm_obj.product, product_model = pm_obj, equipment_status = SnStatus.NORMAL)
                # create equipmentsn
                es_obj = EquipmentSn.create(code = code, last_cal_time = ors_obj.last_cal_time, total_amount = ors_obj.total_amount, \
                                         customer = ors_obj.order.customer, equipment = e_obj, order = ors_obj.order, \
                                         product = pm_obj.product, product_model = pm_obj, sn_status = SnStatus.NORMAL)
                # create serviceitem
                ServiceItem.create(buyinfo_status = ors_obj.buyinfo_status, dsinfo_status = ors_obj.dsinfo_status, \
                                   rebate_status = ors_obj.rebate_status, sn_status = ors_obj.sn_status, \
                                   customer = ors_obj.order.customer, service = s_obj, order = ors_obj.order, \
                                   equipment = e_obj, equipment_sn = es_obj)


        except Exception as e:
            raise BusinessError("数据恢复失败")
        try:
            ors_event.delete()
            ors_obj.delete()
        except Exception as e:
            raise BusinessError("删除退货订单记录失败")

    @classmethod
    def hung_amount_product(cls, ors_qs):
        for ors in ors_qs:
            ors.product = 0
            ors.amount = 0
            try:
                product_model = EquipmentIn.search(min_number__lte = ors.code).filter(max_number__gte = ors.code)[0].product_model
                oi = OrderItem.search(order = ors.order)
                if oi:
                    price = oi[0].price / 100
                ors.product = product_model
                ors.amount = price
            except Exception as e:
                pass
            ors.quantity = 1
            ors.status = '已退货'

    @classmethod
    def hung_department_seller(cls, ors_qs):
        for ors in ors_qs:
            ors.department = ''
            ors.seller = ''
            ors.phone_code = ''
            try:
                sre = StaffReturnsEvent.search(order_returns = ors)[0]
                ors.department = sre.department.name
                ors.seller = sre.staff.name
                ors.phone_code = sre.order_returns.order.customer.mobiledevices.code
            except Exception as e:
                print("------------------>phone_code:", e)

class ReplenishmentServer(object):
    @classmethod
    def get(cls, replenishment_item_id):
        replenishment_item = ReplenishmentItem.get_byid(replenishment_item_id)
        if replenishment_item is None:
            raise BusinessError("该补货单不存在")
        return replenishment_item

    @classmethod
    def search(cls, current_page, **search_info):
        replenishment_item_qs = cls.search_qs(**search_info)
        replenishment_item_qs = replenishment_item_qs.order_by("-create_time")
        return Splitor(current_page, replenishment_item_qs)

    @classmethod
    def search_qs(cls, **search_info):
        if 'consignee' in search_info:
            consignee = search_info.pop('consignee')
            search_info.update({'replenishment__order__consignee': consignee})
        if 'order_sn' in search_info:
            order_sn = search_info.pop('order_sn')
            search_info.update({'replenishment__order__order_sn': order_sn})
        if 'phone' in search_info:
            phone = search_info.pop('phone')
            search_info.update({'replenishment__order__phone__contains': phone})
        if 'shop' in search_info:
            shop = search_info.pop('shop')
            search_info.update({'replenishment__order__shop__name': shop})
        if 'seller' in search_info:
            seller_id = search_info.pop('seller')
            search_info.update({'staff__id': seller_id})
        if 'department' in search_info:
            dept_id = search_info.pop("department")
            dept_list = department_middleware.get_all_children_ids(dept_id)
            dept_list.append(dept_id)
            search_info.update({"department__id__in": dept_list})
        if "create_time_start" in search_info:
            begin_time = search_info.pop("create_time_start")
            search_info.update({"replenishment__create_time__gte": begin_time})
        if "create_time_end" in search_info:
            end_time = search_info.pop("create_time_end")
            search_info.update({"replenishment__create_time__lte": end_time})

        replenishment_event_qs = ReplenishmentEvent.search(**search_info)
        replenishment_qs = [req.replenishment for req in replenishment_event_qs]
        replenishment_item_qs = ReplenishmentItem.search(replenishment__in = replenishment_qs)
        return replenishment_item_qs

    @classmethod
    def hung_all(cls, ri_qs):
        for ri in ri_qs:
            re_obj = ReplenishmentEvent.search(replenishment = ri.replenishment)[0]
            ri.seller = re_obj.staff.name
            ri.department = re_obj.department.name

    @classmethod
    def apply_for(cls, order_sn, order_item, code_list):

        error_list = []
        order_obj = Order.search(order_sn = order_sn)[0]
        replenishmentitem_qs = ReplenishmentItem.search(code__code__in = code_list, replenishment__order = order_obj)
        if replenishmentitem_qs.count() == len(code_list):
            raise BusinessError('请不要重复申请补货')
        # currently no use
        # quantity = len(item_list)
        oe_obj = StaffOrderEvent.search(order = order_obj)[0]
        staff = oe_obj.staff
        department = oe_obj.department
        replenishment_num = ReplenishmentNum().replenishment_num
        rpmtobj = Replenishment.create(order = order_obj, customer = order_obj.customer, replenishment_num = replenishment_num,
                                       quantity = 1)
        ReplenishmentEvent.create(replenishment = rpmtobj, staff = staff, department = department)
        for i, val in enumerate(code_list):
            code = val
            try:
                oi_obj = order_item
                e_obj = Equipment.search(code = code)[0]
                if ReplenishmentItem.search(code = e_obj, replenishment__order = order_obj):
                    error_list.append(code)
                    continue
                g_obj = oi_obj.goods
                # move this part to export ------20180726
                # if order_obj.remark is not None:
                #     remark = order_obj.remark + '   BF:' + code
                # else:
                #     remark = 'BF' + code
                remark = ''
                ReplenishmentItem.create(replenishment = rpmtobj, code = e_obj, goods = g_obj, remark = remark, amount = oi_obj.price,
                                         status = Restatus.WAITING)
            except Exception as _:

                raise BusinessError('申请补货失败,SN码异常')

        return error_list


    @classmethod
    def remove(cls, replenishment_item):

        r_obj = replenishment_item.replenishment
        replenishment_item.delete()
        if ReplenishmentItem.search(replenishment = r_obj).count() == 0:
            ReplenishmentEvent.search(replenishment = r_obj).delete()
            r_obj.delete()


    @classmethod
    def export(cls, ri_id, **search_info):
        if not ri_id:
            ri_qs = cls.search_qs(**search_info)
        else:
              ri_qs = ReplenishmentItem.search(id__in = ri_id)
        # attr_list = ["网店订单编号", "商品名称", "商品编码", "订单状态", "数量", "单价", "订单日期", "收货人名称",
        #              "收货人电话", "收货人手机", "省份", "市", "区", "收货地址", "买家帐号", "物流公司", "物流单号",
        #              "买家运费", "买家留言", "卖家备注", "发票抬头", "订单备注"]
        attr_list_eng = ['order_sn', 'goods_name', 'goods_num', 'order_status', 'quantity', 'price', 'pay_time', 'consignee',
                         'telephone', 'cell_phone', 'province', 'city', 'area', 'address', 'buyer_account',
                         'delivery', 'delivery_num', 'buyer_fee', 'buyer_message', 'seller_remark', 'invoice', 'order_remark']
        result_list = []
        for ri in ri_qs:
            if ri.replenishment and ri.replenishment.order and ri.goods:
                # 查售前客服
                staff_order_event = StaffOrderEvent.search(order = ri.replenishment.order)[0]

                info = []
                order_sn = ri.replenishment.order.order_sn + '_BF' + str(ri.id)
                # info.append(ri.replenishment.order.order_sn)
                info.append(order_sn)
                info.append(ri.goods.name)
                info.append(ri.goods.code)
                info.append(ri.replenishment.order.status)
                info.append(ri.replenishment.order.total_quantity)
                info.append(ri.goods.price)
                info.append(ri.replenishment.order.pay_time)
                info.append(ri.replenishment.order.consignee)
                info.append(ri.replenishment.order.phone)
                info.append(ri.replenishment.order.phone)
                info.append('')
                info.append(ri.replenishment.customer.city)
                info.append('')
                info.append(ri.replenishment.order.address)
                info.append(ri.replenishment.customer.nick)
                info.append('')
                info.append('')
                info.append('')
                info.append('')
                info.append('')
                info.append('')
                remark = "kf{person}kf wx{mobile}wx bz{remark}bz bf{equpment}bf".format(person = staff_order_event.staff.name, \
                                                                               mobile = ri.replenishment.customer.mobiledevices.code, \
                                                                               remark = ri.replenishment.order.remark, \
                                                                               equpment = ri.code.code)

                if remark is not None:
                    remark = remark + '   bf' + ri.code.code + 'bf'
                else:
                    remark = 'bf' + ri.code.code + 'bf'
                info.append(remark)
                temp_dict = dict(zip(attr_list_eng, info))
                result_list.append(temp_dict)
        ri_qs.update(status = Restatus.RESEND)
        return result_list

