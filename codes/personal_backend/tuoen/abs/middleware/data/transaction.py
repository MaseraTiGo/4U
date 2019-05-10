# coding=UTF-8
import datetime
import json
from tuoen.sys.utils.common.timetools import add_month

from tuoen.sys.utils.common.dictwrapper import DictWrapper
from tuoen.sys.core.field.base import BaseField, IntField, \
        CharField, DatetimeField
from tuoen.abs.middleware.data.base import ExcelImport, \
        ExcelDateTimeField, ExcelMoneyField, ExcelDeletePointField
from model.store.model_import import ImportCustomerTransaction, ImportStatus
from model.store.model_equipment_sn import EquipmentSn, SnStatusType
from model.store.model_equipment_register import EquipmentRegister
from model.store.model_equipment_transaction import EquipmentTransaction
from model.store.model_equipment_rebate import EquipmentRebate
from model.store.model_service import ServiceItem
from tuoen.sys.core.exception.business_error import BusinessError

class TransactionImport(ExcelImport):

    def __init__(self):
        self._error_msg = ""
        self._transaction_time = None
        self._equipment_register = None

    def get_exec_cls(self):
        return ImportCustomerTransaction

    def get_redis_name(self):
        return "ImportCustomerTransaction"

    def get_fields(self):
        check_list = [
            ['agent_name', CharField(desc = "代理商名称")],
            ['service_code', CharField(desc = "服务编码")],
            ['code', CharField(desc = "客户编码")],
            ['phone', CharField(desc = "注册手机号")],
            ['transaction_year', ExcelDateTimeField(desc = "交易日期")],
            ['transaction_day', ExcelDeletePointField(desc = "交易时间")],
            ['transaction_code', CharField(desc = "交易流水号")],
            ['transaction_money', ExcelMoneyField(desc = "交易金额/分")],
            ['fee', ExcelMoneyField(desc = "手续费/分")],
            ['good_service_fee', ExcelMoneyField(desc = "优享手续费/分")],
            ['rate', ExcelMoneyField(desc = "客户费率")],
            ['good_service_rate', ExcelMoneyField(desc = "优享费率")],
            ['other_fee', ExcelMoneyField(desc = "其它手续费/分")],
            ['transaction_status', CharField(desc = "交易状态")],
            ['type', CharField(desc = "号段类型")],
        ]
        return check_list

    def skip_repeat(self, code, transaction_time):
        if code not in self._all_equipment_register:
            equipment_register_qs = EquipmentRegister.query().filter(code = code)
            if equipment_register_qs.count() == 0:
                self._error_msg = "客户编码不存在"
                return False
            er = equipment_register_qs[0]
        else:
            er = self._all_equipment_register[code]
        self._equipment_register = er

        """
        equipment_transaction_qs = EquipmentTransaction.query(code = self._equipment_register, \
                                                              transaction_time = transaction_time)
        if equipment_transaction_qs.count() > 0:
            self._error_msg = "数据重复"
            return False
        """

        if (self._equipment_register.id, transaction_time) in self._all_transaction:
            self._error_msg = "数据重复"
            return False

        return True

    def check_data(self, transaction):
        if transaction.transaction_status != "成功":
            self._error_msg = "交易失败无法转化"
            return False
        try:
            transaction_time_str = "{y}{d}".format(y = transaction.transaction_year.strftime("%Y-%m-%d"), d = transaction.transaction_day)
            self._transaction_time = datetime.datetime.strptime(transaction_time_str, '%Y-%m-%d%H%M%S')
        except Exception as e:
            self._error_msg = "交易日期或时间错误"
            return False
        if not self.skip_repeat(transaction.code, self._transaction_time):
            return False

        return True

    def convert_prepare(self, convert_list):
        code_list = []
        min_transation_time = None
        for tr in convert_list:
            code_list.append(tr.code)
            try:
                transaction_time_str = "{y}{d}".format(y = tr.transaction_year.strftime("%Y-%m-%d"), d = tr.transaction_day)
                transaction_time = datetime.datetime.strptime(transaction_time_str, '%Y-%m-%d%H%M%S')
                if min_transation_time is None or min_transation_time > transaction_time:
                    min_transation_time = transaction_time
            except Exception as e:
                continue

        code_list = list(set(code_list))
        self._all_equipment_register = {}
        equipment_sn_id_set = set()
        code_id_set = set()
        for er in EquipmentRegister.query().filter(code__in = code_list):
            self._all_equipment_register[er.code] = er
            if er.equipment_sn_id:
                equipment_sn_id_set.add(er.equipment_sn_id)
            code_id_set.add(er.id)

        equipment_sn_id_list = list(equipment_sn_id_set)
        register_id_list = list(code_id_set)

        self._all_equipment_sn = { equipment_sn.id : equipment_sn for equipment_sn in EquipmentSn.query().filter(id__in = equipment_sn_id_list)}
        self._all_serviceitem = {serviceitem.equipment_sn: serviceitem for serviceitem in
                                 ServiceItem.query().filter(equipment_sn_id__in = equipment_sn_id_list)}

        equipment_transaction_qs = EquipmentTransaction.query()\
                .filter(code_id__in = register_id_list, transaction_time__gte = min_transation_time)
        self._all_transaction = {(et.id, et.transaction_time): et for et in equipment_transaction_qs}

        """
        print('--------->>>>>>', min_transation_time)
        print('---------->>>> ', len(self._all_serviceitem))
        print('---------->>>> ', len(self._all_equipment_register))
        print('---------->>>> ', len(self._all_equipment))
        print('---------->>>> ', len(self._all_transaction))
        print(self._all_transaction)
        """
        return convert_list, []

    def exec_convet(self, transaction):
        check_repeat = self.check_data(transaction)
        if check_repeat:
            rebate_money = self.get_rebate_money(self._equipment_register.equipment_sn_id)
            equipment_transaction = EquipmentTransaction.create(agent_name = transaction.agent_name, service_code = transaction.service_code, \
                                code = self._equipment_register, phone = transaction.phone, transaction_time = self._transaction_time, \
                                transaction_code = transaction.transaction_code, transaction_money = transaction.transaction_money, \
                                fee = transaction.fee, good_service_fee = transaction.good_service_fee, \
                                rate = transaction.rate, good_service_rate = transaction.good_service_rate, \
                                other_fee = transaction.other_fee, \
                                transaction_status = transaction.transaction_status, type = transaction.type, register_code = transaction.code)
            if rebate_money > 0:
                if self._equipment_register.equipment_sn in self._all_serviceitem:
                    service_item = self._all_serviceitem[self._equipment_register.equipment_sn]
                else:
                    service_item_qs = ServiceItem.query(equipment_sn = self._equipment_register.equipment_sn)
                    if service_item_qs.count() > 0:
                        service_item = service_item_qs[0]
                    else:
                        service_item = None
                if service_item is not None:
                    if service_item.rebate_status == SnStatusType.RED:
                        last_time = add_month(self._equipment_register.bind_time, 2)
                        total_money_lastmonth = EquipmentTransaction.sum_money(transaction_time__range = (self._equipment_register.bind_time, last_time), \
                                                                               code = self._equipment_register)
                        if total_money_lastmonth >= rebate_money:
                           equipment_rebate_qs = EquipmentRebate.query().filter(code = self._equipment_register, remark__contains = "已达到")
                           if equipment_rebate_qs.count() > 0:
                               service_item.update(rebate_status = SnStatusType.TGREEB)
                           else:
                               service_item.update(rebate_status = SnStatusType.GREEN)
                        else:
                            total_money = EquipmentTransaction.sum_money(code = self._equipment_register)
                            if total_money >= rebate_money:
                                service_item.update(rebate_status = SnStatusType.YELLOW)
            return True, ""

        return False, self._error_msg

    def get_rebate_money(self, equipment_sn_id):
        if equipment_sn_id:
            if equipment_sn_id in self._all_equipment_sn:
                equipment_sn = self._all_equipment_sn[equipment_sn_id]
            else:
                equipment_sn = EquipmentSn.get_byid(equipment_sn_id)

            if equipment_sn is not None:
                if equipment_sn.product is not None:
                    return equipment_sn.product.rebate_money


        return 0

    def reset_status(self, **search_info):
        search_info.update({'status__in': [ImportStatus.EXCUTTING, ImportStatus.FAILED]})
        if "create_time_start" in search_info:
            search_info.update({'create_time__gte': search_info.pop("create_time_start")})
        if "create_time_end" in search_info:
            search_info.update({'create_time__lt': search_info.pop("create_time_end")})
        try:
            ImportCustomerTransaction.search(**search_info).update(status = ImportStatus.INIT, error_text = '')
        except Exception as e:
            raise  BusinessError("恢復初始化失敗")

