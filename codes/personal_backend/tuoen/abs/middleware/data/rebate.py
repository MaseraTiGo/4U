# coding=UTF-8
import json
from tuoen.sys.utils.common.dictwrapper import DictWrapper
from tuoen.sys.core.field.base import BaseField, IntField, \
        CharField, DatetimeField
from tuoen.abs.middleware.data.base import ExcelImport, \
        ExcelDateTimeField, ExcelMoneyField
from model.store.model_import import ImportCustomerRebate, ImportStatus
from model.store.model_equipment_register import EquipmentRegister
from model.store.model_equipment_rebate import EquipmentRebate
from model.store.model_service import ServiceItem
from model.store.model_equipment_sn import SnStatusType
from tuoen.sys.core.exception.business_error import BusinessError

class RebateImport(ExcelImport):

    def __init__(self):
        self._error_msg = ""
        self._equipment_register = None

    def get_exec_cls(self):
        return ImportCustomerRebate

    def get_redis_name(self):
        return "ImportCustomerRebate"

    def get_fields(self):
        check_list = [
            ['agent_id', CharField(desc = "代理商ID")],
            ['agent_name', CharField(desc = "代理商名称")],
            ['code', CharField(desc = "客户编码")],
            ['name', CharField(desc = "客户名称")],
            ['phone', CharField(desc = "注册手机号")],
            ['activity_type', CharField(desc = "活动类型")],
            ['is_silent', CharField(desc = "是否为沉默用户")],
            ['device_code', CharField(desc = "设备编码")],
            ['register_time', ExcelDateTimeField(desc = "注册时间")],
            ['bind_time', ExcelDateTimeField(desc = "绑定时间")],
            ['month', ExcelDateTimeField(desc = "交易月份")],
            ['transaction_amount', ExcelMoneyField(desc = "交易金额/分")],
            ['effective_amount', ExcelMoneyField(desc = "有效金额/分")],
            ['accumulate_amount', ExcelMoneyField(desc = "当月累计交易金额/分")],
            ['history_amount', ExcelMoneyField(desc = "历史累计交易金额/分")],
            ['type', CharField(desc = "号段类型")],
            ['is_rebate', CharField(desc = "是否返利")],
            ['remark', CharField(desc = "备注")],
            ['activation_date', ExcelDateTimeField(desc = "激活日期")],
        ]
        return check_list

    def skip_repeat(self, code, month):
        if code not in self._all_code_register:
            self._error_msg = "客户id不存在"
            return False
        self._equipment_register = self._all_code_register[code]

        if (self._equipment_register.id, month) in self._all_rebase:
            self._error_msg = "数据重复"
            """
            print('===============================================>>> 数据重复')
            """
            return False

        return True

    def convert_prepare(self, convert_list):
        code_list = []
        min_month = None
        for tr in convert_list:
            code_list.append(tr.code)
            if min_month is None or min_month > tr.month:
                min_month = tr.month

        self._all_code_register = {}
        self._all_equipment_register = {}
        for er in EquipmentRegister.query().filter(code__in = code_list):
            self._all_code_register[er.code] = er
            if er.equipment_sn:
                self._all_equipment_register[er.equipment_sn] = er

        self._all_serviceitem = {serviceitem.equipment_sn: serviceitem for serviceitem in
                                 ServiceItem.query().filter(equipment_sn__in = self._all_equipment_register.keys())}
        equipment_rebate_qs = EquipmentRebate.query()\
                .filter(code__in = self._all_code_register.values(), month__gte = min_month)
        self._all_rebase = {(er.code_id, er.month): er for er in equipment_rebate_qs}
        return convert_list, []

    def exec_convet(self, rebate):
        check_repeat = self.skip_repeat(rebate.code, rebate.month)
        if check_repeat:
            EquipmentRebate.create(agent_id = rebate.agent_id, agent_name = rebate.agent_name, \
                                       code = self._equipment_register, name = rebate.name, phone = rebate.phone, \
                                       activity_type = rebate.activity_type, register_time = rebate.register_time, \
                                       bind_time = rebate.bind_time, month = rebate.month, transaction_amount = rebate.transaction_amount, \
                                       effective_amount = rebate.effective_amount, accumulate_amount = rebate.accumulate_amount, \
                                       history_amount = rebate.history_amount, type = rebate.type, is_rebate = rebate.is_rebate, \
                                       remark = rebate.remark, register_code = rebate.code);
            if "已达到" in rebate.remark:
                if self._equipment_register.equipment_sn in self._all_serviceitem:
                    service_item = self._all_serviceitem[self._equipment_register.equipment_sn]
                else:
                    service_item_qs = ServiceItem.query(equipment_sn = self._equipment_register.equipment_sn)
                    if service_item_qs.count() > 0:
                        service_item = service_item_qs[0]
                    else:
                        service_item = None

                if service_item is not None:
                    if service_item.rebate_status == SnStatusType.GREEN:
                        service_item.update(rebate_status = SnStatusType.TGREEB)

            return True, ""

        return False, self._error_msg

    def reset_status(self, **search_info):
        search_info.update({'status__in': [ImportStatus.EXCUTTING, ImportStatus.FAILED]})
        if "create_time_start" in search_info:
            search_info.update({'create_time__gte': search_info.pop("create_time_start")})
        if "create_time_end" in search_info:
            search_info.update({'create_time__lt': search_info.pop("create_time_end")})
        try:
            ImportCustomerRebate.search(**search_info).update(status = ImportStatus.INIT, error_text = '')
        except Exception as e:
            raise  BusinessError("恢復初始化失敗")
