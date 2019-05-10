# coding=UTF-8
import hashlib
import json
from tuoen.sys.utils.common.dictwrapper import DictWrapper
from tuoen.sys.core.field.base import BaseField, IntField, \
        CharField, DatetimeField
from tuoen.abs.middleware.data.base import ExcelImport, \
        ExcelDateTimeField, ExcelMoneyField, ExcelDeletePointField
from model.store.model_import import ImportStaff, ImportStatus
from model.store.model_user import Staff, GenderTypes, EducationType
from model.store.model_account import StaffAccount
from model.store.model_role import Role
from model.store.model_department import Department
from model.store.model_auth_access import AuthAccess, AccessTypes

from tuoen.sys.core.exception.business_error import BusinessError


class StaffImport(ExcelImport):

    def __init__(self):
        self._error_msg = ""

    def get_exec_cls(self):
        return ImportStaff

    def get_redis_name(self):
        return "ImportStaff"

    def get_fields(self):
        check_list = [
            ['name', CharField(desc = "姓名")],
            ['position', CharField(desc = "职位")],
            ['department', CharField(desc = "部门")],
            ['phone', ExcelDeletePointField(desc = "手机号")],
            ['gender', CharField(desc = "性别")],
            ['identity', CharField(desc = "身份证号")],
            ['birthday', ExcelDateTimeField(desc = "生日")],
            ['age', IntField(desc = "年龄")],
            ['emergency_contact', CharField(desc = "紧急联系人")],
            ['emergency_phone', ExcelDeletePointField(desc = "紧急联系人电话")],
            ['address', CharField(desc = "详细地址")],
            ['entry_time', ExcelDateTimeField(desc = "入职时间")],
            ['education', CharField(desc = "学历")],
            ['bank_number', CharField(desc = "招行卡号")],
            ['contract_b', CharField(desc = "合同编号（必）")],
            ['contract_l', CharField(desc = "合同编号（立）")],
            ['expire_time', ExcelDateTimeField(desc = "到期时间")],
            ['is_on_job', CharField(desc = "是否离职")],
            ['quit_time', ExcelDateTimeField(desc = "离职时间")],
            ['remark', CharField(desc = "备注")],
        ]
        return check_list


    def skip_staff(self, name, identity, is_on_job):
        if name == "":
            self._error_msg = "缺少姓名"
            return False

        if identity == "":
            staff_qs = Staff.search(name = name)
        else:
            staff_qs = Staff.search(name = name, identity = identity)

        if staff_qs.count() > 0:
            self._error_msg = "重复数据"
            return False

        return True

    def exec_convet(self, importstaff):

        check_staff = self.skip_staff(importstaff.name, importstaff.identity, importstaff.is_on_job)
        if check_staff:
            staff = Staff.create(name = importstaff.name, phone = importstaff.phone[:11], gender = self.get_gender(importstaff.gender), \
                                 identity = importstaff.identity, birthday = importstaff.birthday, \
                                 emergency_contact = importstaff.emergency_contact, emergency_phone = importstaff.emergency_phone[:11], \
                                 address = importstaff.address, entry_time = importstaff.entry_time , \
                                 education = self.get_education(importstaff.education), bank_number = importstaff.bank_number , \
                                 contract_b = importstaff.contract_b, contract_l = importstaff.contract_l, \
                                 expire_time = importstaff.expire_time, remark = importstaff.remark, \
                                 quit_time = importstaff.quit_time, is_working = self.get_is_working(importstaff.is_on_job), \
                                 )
            if staff is not None and staff.is_working:
                if staff.phone:
                    staff_account_qs = StaffAccount.query().filter(username = staff.phone)
                    if staff_account_qs.count() == 0:
                        StaffAccount.create(username = staff.phone, password = hashlib.md5("123456".encode("utf-8")).hexdigest(), \
                                        staff = staff)
            self.convet_role(staff, importstaff.position)
            self.convet_department(staff, importstaff.department)

            return True, ""

        return False, self._error_msg

    def get_gender(self, gender):
        switch = {
            "男":GenderTypes.MAN,
            "女":GenderTypes.WOMAN,
            "未知":GenderTypes.UNKNOWN,
        }
        try:
            return switch[gender]
        except Exception as e:
            return "unknown"

    def get_education(self, education):
        switch = {
            "小学":EducationType.PRIMARY,
            "初中":EducationType.MIDDLE,
            "高中":EducationType.HIGH,
            "本科":EducationType.UNDERGRADUAYE,
            "大专":EducationType.COLLEGE,
            "中专":EducationType.MIDDLECOLLEGE,
            "硕士":EducationType.MASTER,
            "博士":EducationType.DOCTOR,
            "其他":EducationType.OTHER,
        }
        try:
            return switch[education]
        except Exception as e:
            return ""

    def get_is_working(self, is_on_job):
        if is_on_job == "在职":
            return True
        else:
            return False

    def convet_role(self, staff, role_name):
        role_name_list = role_name.split("##")
        role_qs = Role.search(name__in = role_name_list)
        if role_qs.count() > 0:
            for role in role_qs:
                AuthAccess.create(staff = staff, access_id = role.id, access_type = AccessTypes.ROLE)

    def convet_department(self, staff, department_name):
        department_name_list = department_name.split("##")
        department_qs = Department.search(name__in = department_name_list)
        if department_qs.count() > 0:
            for department in department_qs:
                AuthAccess.create(staff = staff, access_id = department.id, access_type = AccessTypes.DEPARTMENT)

    def reset_status(self, **search_info):
        search_info.update({'status__in': [ImportStatus.EXCUTTING, ImportStatus.FAILED]})
        if "create_time_start" in search_info:
            search_info.update({'create_time__gte': search_info.pop("create_time_start")})
        if "create_time_end" in search_info:
            search_info.update({'create_time__lt': search_info.pop("create_time_end")})
        try:
            ImportStaff.search(**search_info).update(status = ImportStatus.INIT, error_text = '')
        except Exception as e:
            raise  BusinessError("恢復初始化失敗")
