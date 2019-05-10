# coding=UTF-8
import hashlib
import json
from tuoen.sys.utils.common.dictwrapper import DictWrapper
from tuoen.sys.core.field.base import BaseField, IntField, \
        CharField, DatetimeField
from tuoen.abs.middleware.data.base import ExcelImport, \
        ExcelDateTimeField, ExcelMoneyField, ExcelDeletePointField
from model.store.model_import import ImportMobileDevices, ImportStatus
from model.store.model_mobilephone import MobileDevices, Mobilephone, MobileDeviceStatus, MobileMaintain
from model.store.model_user import Staff
from model.models import Department
from tuoen.sys.core.exception.business_error import BusinessError
from tuoen.abs.middleware.department import department_middleware

class MobileDevicesImport(ExcelImport):

    def __init__(self):
        self._error_msg = ""

    def get_exec_cls(self):
        return ImportMobileDevices

    def get_redis_name(self):
        return "ImportMobileDevices"


    def get_fields(self):
        check_list = [
            ['group_leader', CharField(desc = "負責人")],
            ['mobile_code', ExcelDeletePointField(desc = "手机编号")],
            ['group_member', CharField(desc = "组员姓名")],
            ['wechat_nick', CharField(desc = "微信昵称")],
            ['wechat_number', CharField(desc = "微信号")],
            ['wechat_password', CharField(desc = "微信密码")],
            ['pay_password', ExcelDeletePointField(desc = "微信支付密码")],
            ['wechat_remark', CharField(desc = "微信号备注")],
            ['department', CharField(desc = "部门")],
            ['phone_number', ExcelDeletePointField(desc = "手机号")],
            ['operator', CharField(desc = "运营商")],
            ['real_name', CharField(desc = "实名人姓名")],
            ['phone_remark', CharField(desc = "手机号备注")],
            ['flow_card_number', CharField(desc = "流量卡号")],
            ['imei', CharField(desc = "手机imei号")],
            ['brand', CharField(desc = "手机品牌")],
            ['model', CharField(desc = "手机型号")],
            ['price', ExcelMoneyField(desc = "购买价格/分")],
            ['mobile_status', CharField(desc = "手机设备状态")],
            ['mobile_remark', CharField(desc = "手机设备备注")],
            ['phone_change', CharField(desc = "手机变更信息")],
        ]
        return check_list


    def skip_mobile_devices(self, mobile_code, department_name):
        devices = None
        department = None
        department_qs = Department.search(name = department_name)
        if department_qs.count() > 0:
            department = department_qs[0]
        else:
            department = Department.search(name = "其他")[0]

        devices_qs = MobileDevices.search(code = mobile_code)
        if devices_qs.count() > 0:
            devices = devices_qs[0]

        return devices, department

    def exec_convet(self, mobile_devices):
        department_name = mobile_devices.department
        department_name = department_name.strip()

        devices, department = self.skip_mobile_devices(mobile_devices.mobile_code, department_name)

        if devices is not None:
            devices.update(brand = mobile_devices.brand, \
                      model = mobile_devices.model, price = mobile_devices.price, \
                      status = self.get_devices_status(mobile_devices.mobile_status), \
                      remark = self.get_mobile_devices_remark(mobile_devices.mobile_remark, mobile_devices.department), \
                      imei = mobile_devices.imei, \
                                      )
        else:
            devices = MobileDevices.create(code = mobile_devices.mobile_code, brand = mobile_devices.brand, \
                                           model = mobile_devices.model, price = mobile_devices.price, \
                                           status = self.get_devices_status(mobile_devices.mobile_status), \
                                           remark = self.get_mobile_devices_remark(mobile_devices.mobile_remark,
                                                                                 mobile_devices.department), \
                                           imei = mobile_devices.imei, \
                                           )
        mobile_phone_staff = self.get_staff(mobile_devices.real_name)
        mp = Mobilephone.search(devices = devices)
        if mp:
            mp.update(leader = mobile_devices.group_leader, t_member = mobile_devices.group_member, \
                               staff = mobile_phone_staff, name = mobile_devices.real_name, \
                               identity = mobile_phone_staff.identity if mobile_phone_staff else "", \
                               wechat_nick = mobile_devices.wechat_nick, \
                               wechat_number = mobile_devices.wechat_number,
                               wechat_password = mobile_devices.wechat_password, \
                               pay_password = mobile_devices.pay_password, wechat_remark = mobile_devices.wechat_remark, \
                               phone_number = mobile_devices.phone_number, operator = mobile_devices.operator, \
                               phone_remark = mobile_devices.phone_remark,
                               flow_card_number = mobile_devices.flow_card_number, \
                               department = department, phone_change = mobile_devices.phone_change
                               )
        else:
            Mobilephone.create(leader = mobile_devices.group_leader, t_member = mobile_devices.group_member, \
                               devices = devices, staff = mobile_phone_staff, name = mobile_devices.real_name, \
                               identity = mobile_phone_staff.identity if mobile_phone_staff else "",
                               wechat_nick = mobile_devices.wechat_nick, \
                               wechat_number = mobile_devices.wechat_number,
                               wechat_password = mobile_devices.wechat_password, \
                               pay_password = mobile_devices.pay_password,
                               wechat_remark = mobile_devices.wechat_remark, \
                               phone_number = mobile_devices.phone_number, operator = mobile_devices.operator, \
                               phone_remark = mobile_devices.phone_remark,
                               flow_card_number = mobile_devices.flow_card_number, \
                               department = department, phone_change = mobile_devices.phone_change
                               )
        return True, self._error_msg

    def get_mobile_phone(self, phone_number):
        mobile_phone = None
        mobile_phone_qs = Mobilephone.query().filter(phone_number = phone_number)
        if mobile_phone_qs.count() > 0:
            mobile_phone = mobile_phone_qs[0]

        return mobile_phone

    def get_devices_status(self, mobile_status):
        switch = {
            "正常":MobileDeviceStatus.NORMAL,
            "报废":MobileDeviceStatus.SCRAP,
            "闲置":MobileDeviceStatus.IDLE,
            "其它":MobileDeviceStatus.OTHER,
        }
        try:
            return switch[mobile_status]
        except Exception as e:
            return MobileDeviceStatus.OTHER


    def get_staff(self, staff_name):
        staff = Staff.get_staff_byname(staff_name)

        return staff

    def get_mobile_devices_remark(self, mobile_remark, department):
        if department:
            return "{a}({b})".format(a = mobile_remark, b = department)

        return mobile_remark

    def get_mobile_maintain_remark(self, group_leader):
        if group_leader:
            return "leader:{a};".format(a = group_leader)

        return ""
    def reset_status(self, **search_info):
        search_info.update({'status__in': [ImportStatus.EXCUTTING, ImportStatus.FAILED]})
        if "create_time_start" in search_info:
            search_info.update({'create_time__gte': search_info.pop("create_time_start")})
        if "create_time_end" in search_info:
            search_info.update({'create_time__lt': search_info.pop("create_time_end")})
        try:
            ImportMobileDevices.search(**search_info).update(status = ImportStatus.INIT, error_text = '')
        except Exception as e:
            raise  BusinessError("恢復初始化失敗")
