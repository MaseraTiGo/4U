# coding=UTF-8
import hashlib
import json
from tuoen.sys.utils.common.dictwrapper import DictWrapper
from tuoen.sys.core.field.base import BaseField, IntField, \
        CharField, DatetimeField
from tuoen.abs.middleware.data.base import ExcelImport, \
        ExcelDateTimeField, ExcelMoneyField, ExcelDeletePointField
from model.store.model_import import ImportMobilePhone, ImportStatus
from model.store.model_mobilephone import Mobilephone, MobileStatus
from model.store.model_user import Staff
from model.store.model_department import Department

from tuoen.sys.core.exception.business_error import BusinessError

class MobilephoneImport(ExcelImport):

    def __init__(self):
        self._error_msg = ""
        self._mobile_phone = None

    def get_exec_cls(self):
        return ImportMobilePhone

    def get_redis_name(self):
        return "ImportMobilePhone"

    def get_fields(self):
        check_list = [
            ['name', CharField(desc = "姓名")],
            ['identity', CharField(desc = "身份证号")],
            ['phone_number', ExcelDeletePointField(desc = "手机号码")],
            ['department', CharField(desc = "部门")],
            ['is_working', CharField(desc = "在职情况")],
            ['card_password', ExcelDeletePointField(desc = "手机卡密码")],
            ['operator', CharField(desc = "运营商")],
            ['rent', ExcelMoneyField(desc = "月租")],
            ['phone_status', CharField(desc = "手机号状态")],
            ['phone_remark', CharField(desc = "手机号备注")],
        ]
        return check_list

    def skip_mobile_phone(self, phone_number):
        if not phone_number:
            self._error_msg = "缺少手机号"
            return False

        mobile_phone_qs = Mobilephone.query().filter(phone_number = phone_number)
        if mobile_phone_qs.count() > 0:
            self._mobile_phone = mobile_phone_qs[0]

        return True

    def exec_convet(self, import_mobile_phone):

        check_phone = self.skip_mobile_phone(import_mobile_phone.phone_number)

        if not check_phone:
            return False, self._error_msg

        staff = self.get_staff(import_mobile_phone.name)

        if self._mobile_phone is None:
            Mobilephone.create(staff = staff, name = import_mobile_phone.name, \
                              identity = staff.identity if staff is not None else import_mobile_phone.identity, \
                              phone_number = import_mobile_phone.phone_number, \
                              card_password = import_mobile_phone.card_password, operator = import_mobile_phone.operator, \
                              rent = import_mobile_phone.rent, status = self.get_phone_status(import_mobile_phone.phone_status), \
                              phone_remark = self.get_remark(import_mobile_phone.phone_remark, import_mobile_phone.department) , \
                              )
        else:
            self._mobile_phone.update(staff = staff, name = import_mobile_phone.name, \
                                identity = staff.identity if staff is not None else import_mobile_phone.identity, \
                                phone_number = import_mobile_phone.phone_number, \
                                card_password = import_mobile_phone.card_password, operator = import_mobile_phone.operator, \
                                rent = import_mobile_phone.rent, status = self.get_phone_status(import_mobile_phone.phone_status), \
                                phone_remark = self.get_remark(import_mobile_phone.phone_remark, import_mobile_phone.department) , \
                                )

        return True, ""

    def get_staff(self, staff_name):
        staff = Staff.get_staff_byname(staff_name)

        return staff

    def get_phone_status(self, phone_status):
        if phone_status == "正常":
            return MobileStatus.NORMAL
        elif phone_status == "冻结":
            return MobileStatus.FROZEN
        elif phone_status == "封号":
            return MobileStatus.SEAL
        elif phone_status == "欠费":
            return MobileStatus.ARREARS
        elif phone_status == "停用":
            return MobileStatus.DISCONTINUATION
        else:
            return MobileStatus.OTHER

    def get_remark(self, phone_remark, department):
        if department:
            return "{a}({b})".format(a = phone_remark, b = department)
        else:
            return phone_remark

    def reset_status(self, **search_info):
        search_info.update({'status__in': [ImportStatus.EXCUTTING, ImportStatus.FAILED]})
        if "create_time_start" in search_info:
            search_info.update({'create_time__gte': search_info.pop("create_time_start")})
        if "create_time_end" in search_info:
            search_info.update({'create_time__lt': search_info.pop("create_time_end")})
        try:
            ImportMobilePhone.search(**search_info).update(status = ImportStatus.INIT, error_text = '')
        except Exception as e:
            raise  BusinessError("恢復初始化失敗")
