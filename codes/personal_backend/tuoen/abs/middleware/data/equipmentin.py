# coding=UTF-8
import json
from tuoen.sys.utils.common.dictwrapper import DictWrapper
from tuoen.sys.core.field.base import BaseField, IntField, \
        CharField, DatetimeField
from tuoen.abs.middleware.data.base import ExcelImport, \
        ExcelDateTimeField, ExcelMoneyField
from model.store.model_import import ImportEquipmentIn, ImportStatus
from model.store.model_equipment_in import EquipmentIn
from model.store.model_product import ProductModel
from tuoen.sys.core.exception.business_error import BusinessError

class EquipmentInImport(ExcelImport):

    def __int__(self):
        self._error_msg = ""

    def get_exec_cls(self):
        return ImportEquipmentIn

    def get_redis_name(self):
        return "ImportEquipmentIn"

    def get_fields(self):
        check_list = [
            ['add_time', ExcelDateTimeField(desc = "添加时间")],
            ['agent_name', CharField(desc = "代理商名称")],
            ['product_type', CharField(desc = "产品类型")],
            ['product_model', CharField(desc = "产品型号")],
            ['min_number', IntField(desc = "起始号段")],
            ['max_number', IntField(desc = "终止号段")],
            ['quantity', IntField(desc = "入库数量")],
            ['remark', CharField(desc = "到货备注")],
        ]
        return check_list


    def skip_equipment_in(self, min_number, max_number, product_model):
        if not min_number:
            self._error_msg = "缺少起始号段"
            return False

        if not max_number:
            self._error_msg = "缺少终止号段"
            return False

        equipment_in_min_qs = EquipmentIn.search(min_number__lte = min_number, \
                                          max_number__gte = min_number)
        if equipment_in_min_qs.count() > 0:
            self._error_msg = "起始号段重复"
            return False
        equipment_in_max_qs = EquipmentIn.search(min_number__lte = max_number, \
                                          max_number__gte = max_number)
        if equipment_in_max_qs.count() > 0:
            self._error_msg = "终止号段重复"
            return False

        product_model_qs = ProductModel.query().filter(name = product_model)
        if product_model_qs.count() == 0:
             self._error_msg = "此产品型号不存在"
             return False

        return True

    def exec_convet(self, equipmentin):
        check_equipment_in = self.skip_equipment_in(equipmentin.min_number, equipmentin.max_number, equipmentin.product_model)
        if check_equipment_in:
            EquipmentIn.create(add_time = equipmentin.add_time, agent_name = equipmentin.agent_name, \
                               product_type = equipmentin.product_type, product_model = equipmentin.product_model, \
                               min_number = equipmentin.min_number, max_number = equipmentin.max_number, \
                               quantity = equipmentin.quantity, remark = equipmentin.remark)
            return True, ""

        return False, self._error_msg

    def reset_status(self, **search_info):
        search_info.update({'status__in': [ImportStatus.EXCUTTING, ImportStatus.FAILED]})
        if "create_time_start" in search_info:
            search_info.update({'create_time__gte': search_info.pop("create_time_start")})
        if "create_time_end" in search_info:
            search_info.update({'create_time__lt': search_info.pop("create_time_end")})
        try:
            ImportEquipmentIn.search(**search_info).update(status = ImportStatus.INIT, error_text = '')
        except Exception as e:
            raise  BusinessError("恢復初始化失敗")
