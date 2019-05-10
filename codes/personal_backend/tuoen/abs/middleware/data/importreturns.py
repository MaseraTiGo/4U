# coding=UTF-8
import json
from tuoen.sys.utils.common.dictwrapper import DictWrapper
from tuoen.sys.core.field.base import BaseField, IntField, \
        CharField, DatetimeField
from tuoen.abs.middleware.data.base import ExcelImport, \
        ExcelDateTimeField, ExcelMoneyField
from model.store.model_import import ImportReturns, ImportStatus
from model.store.model_equipment import Equipment, EquipmentStatusState
from model.store.model_equipment_register import EquipmentRegister
from model.store.model_service import Service
from model.store.model_service import ServiceItem
from model.store.model_orderreturns import OrderReturns, ReturnsNum
from model.store.model_order import Order
from model.store.model_order_event import StaffOrderEvent
from tuoen.sys.core.exception.business_error import BusinessError
from model.models import EquipmentSn, SnStatus
from model.store.model_returnsevent import StaffReturnsEvent
from model.store.model_department import Department
from model.store.model_logistics import LogisticsItem
from model.store.model_equipment_in import EquipmentIn
from model.store.model_product import Product, ProductModel
from model.store.model_auth_access import AuthAccess
from model.store.model_department import Department

class ReturnsImport(ExcelImport):
    def __init__(self):
        self._error_msg = ""
        self._code_list = None

    def get_exec_cls(self):
        return ImportReturns

    def get_redis_name(self):
        return "ImportReturns"

    def get_fields(self):
        check_list = [
            ['code', CharField(desc = "设备SN码")]
        ]
        return check_list

    def handle_device_code(self, device_code):

        device_code = device_code.strip()
        device_code_len = len(device_code)
        if device_code_len == 19:
            device_code = device_code[4:]
        elif device_code_len == 20:
            device_code = device_code[4:-1]
        else:
            self._error_msg = "该设备编码位数异常"
            return False, 0

        return True, device_code

    '''
    def convert_prepare(self, convert_list):
        code_list = [ tr.code for tr in convert_list]
        self._code_list = code_list
    '''

    def exec_convet(self, returns):
        update_info = {'customer': None, 'logistics_item': None, 'order': None, }
        hand, code = self.handle_device_code(returns.code)
        if not hand:
            return False, self._error_msg

        equipmentsn_qs = EquipmentSn.query(code = code)
        if equipmentsn_qs.count() > 0:
            esn = equipmentsn_qs[0]
            equipment_register_qs = EquipmentRegister.query(equipment_sn = esn)
            self.insert_order_returns(code)
            if equipment_register_qs.count() > 0:
                esn.update(sn_status = SnStatus.RGOODS)
                esn.equipment.update(**update_info)
            else:
                self.del_service_item(esn)
                esn.equipment.delete()
                esn.delete()



            return True, ""
        else:
            self._error_msg = "设备SN码不存在"

        return False, self._error_msg


    def del_service_item(self, eq):
        service_item_qs = ServiceItem.query(equipment_sn = eq)
        if service_item_qs.count() > 0:
            service_item = service_item_qs[0]
            # 20180711 morning--- after discussion, they decide not to remove this event.
            # if service_item.order:
            #    StaffOrderEvent.query(order = service_item.order).delete()
            service_item.delete()
            if ServiceItem.query(service = service_item.service).count() == 0:
                service_item.service.delete()

    def insert_order_returns(self, code):
        ors = None
        department = None
        staff = None
        server = None
        remark = ''
        buyinfo_status = ''
        dsinfo_status = ''
        rebate_status = ''
        sn_status = ''
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
                                      returns_num = ReturnsNum().returns_num)
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
        else:
            raise BusinessError("创建退货单失败，请检查设备编码")
        return ors

    def reset_status(self, **search_info):
        search_info.update({'status__in': [ImportStatus.EXCUTTING, ImportStatus.FAILED]})
        if "create_time_start" in search_info:
            search_info.update({'create_time__gte': search_info.pop("create_time_start")})
        if "create_time_end" in search_info:
            search_info.update({'create_time__lt': search_info.pop("create_time_end")})
        try:
            ImportReturns.search(**search_info).update(status = ImportStatus.INIT, error_text = '')
        except Exception as e:
            raise  BusinessError("回复初始化失败")
