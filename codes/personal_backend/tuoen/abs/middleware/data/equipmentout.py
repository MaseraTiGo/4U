# coding=UTF-8
import json
from tuoen.sys.utils.common.dictwrapper import DictWrapper
from tuoen.sys.core.field.base import BaseField, IntField, \
        CharField, DatetimeField
from tuoen.abs.middleware.data.base import ExcelImport, \
        ExcelDateTimeField, ExcelMoneyField, ExcelDeletePointField
from model.store.model_import import ImportEquipmentOut, ImportStatus
from model.store.model_equipment_out import EquipmentOut, AgentTypes
from model.store.model_product import ProductModel

from tuoen.sys.core.exception.business_error import BusinessError

class EquipmentOutImport(ExcelImport):

    def __int__(self):
        self._error_msg = ""
        self._type = ""

    def get_exec_cls(self):
        return ImportEquipmentOut

    def get_redis_name(self):
        return "ImportEquipmentOut"

    def get_fields(self):
        check_list = [
            ['add_time', ExcelDateTimeField(desc = "添加时间")],
            ['agent_name', CharField(desc = "代理商名称")],
            ['agent_phone', ExcelDeletePointField(desc = "代理商电话")],
            ['product_type', CharField(desc = "产品类型")],
            ['product_model', CharField(desc = "产品型号")],
            ['min_number', IntField(desc = "起始号段")],
            ['max_number', IntField(desc = "终止号段")],
            ['quantity', IntField(desc = "入库数量")],
            ['price', ExcelDeletePointField(desc = "单价")],
            ['salesman', CharField(desc = "业务员")],
            ['type', CharField(desc = "出库类型")],
            ['address', CharField(desc = "发货地址")],
            ['rate', CharField(desc = "签约费率")],
            ['remark', CharField(desc = "到货备注")],
        ]
        return check_list

    def skip_equipment_out(self, min_number, max_number, product_model, type):
        if not self.convet_type(type):
            return False

        if not min_number:
            self._error_msg = "缺少起始号段"
            return False

        if not max_number:
            self._error_msg = "缺少终止号段"
            return False

        equipment_out_min_qs = EquipmentOut.search(min_number__lte = min_number, \
                                          max_number__gte = min_number)
        if equipment_out_min_qs.count() > 0:
            self._error_msg = "起始号段重复"
            return False
        equipment_out_max_qs = EquipmentOut.search(min_number__lte = max_number, \
                                          max_number__gte = max_number)
        if equipment_out_max_qs.count() > 0:
            self._error_msg = "终止号段重复"
            return False

        product_model_qs = ProductModel.query().filter(name = product_model)
        if product_model_qs.count() == 0:
             self._error_msg = "此产品型号不存在"
             return False

        return True

    def exec_convet(self, equipmentout):
        check_equipment_out = self.skip_equipment_out(equipmentout.min_number, equipmentout.max_number, \
                                                      equipmentout.product_model, equipmentout.type)
        if check_equipment_out:
            EquipmentOut.create(add_time = equipmentout.add_time, agent_name = equipmentout.agent_name, \
                                agent_phone = equipmentout.agent_phone, product_type = equipmentout.product_type, \
                                product_model = equipmentout.product_model, min_number = equipmentout.min_number, \
                                max_number = equipmentout.max_number, quantity = equipmentout.quantity, \
                                price = equipmentout.price, salesman = equipmentout.salesman, \
                                address = equipmentout.address, rate = equipmentout.rate, \
                                remark = equipmentout.remark, type = self._type)
            return True, ""
        return False, self._error_msg

    def reset_status(self, **search_info):
        search_info.update({'status__in': [ImportStatus.EXCUTTING, ImportStatus.FAILED]})
        if "create_time_start" in search_info:
            search_info.update({'create_time__gte': search_info.pop("create_time_start")})
        if "create_time_end" in search_info:
            search_info.update({'create_time__lt': search_info.pop("create_time_end")})
        try:
            ImportEquipmentOut.search(**search_info).update(status = ImportStatus.INIT, error_text = '')
        except Exception as e:
            raise  BusinessError("恢復初始化失敗")

    def convet_type(self, type):
        if type == "自营平台":
            self._type = AgentTypes.SELF
            return True
        elif type == "一级代理":
            self._type = AgentTypes.FIRST
            return True
        elif type == "二级代理":
            self._type = AgentTypes.SECOND
            return True
        else:
            self._error_msg = "出库类型错误"
            return False
