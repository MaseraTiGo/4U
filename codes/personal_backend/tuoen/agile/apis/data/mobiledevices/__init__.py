# coding=UTF-8

import json
from tuoen.sys.core.field.base import CharField, DictField, \
        IntField, ListField, DatetimeField, FileField, DateField, BooleanField
from tuoen.sys.core.api.utils import with_metaclass
from tuoen.sys.core.api.request import RequestField, RequestFieldSet
from tuoen.sys.core.api.response import ResponseField, ResponseFieldSet
from tuoen.sys.core.exception.business_error import BusinessError

from tuoen.agile.apis.base import StaffAuthorizedApi
from tuoen.abs.middleware.data import import_mobile_devices_middleware
import datetime
from model.store.model_journal import JournalTypes, OperationTypes
from tuoen.abs.middleware.journal import JournalMiddleware

import datetime
from model.store.model_journal import JournalTypes, OperationTypes
from tuoen.abs.middleware.journal import JournalMiddleware

class Upload(StaffAuthorizedApi):
    """手机设备导入数据接口"""
    request = with_metaclass(RequestFieldSet)
    request._upload_files = RequestField(FileField, desc = "上传文件")

    response = with_metaclass(ResponseFieldSet)
    response.total = ResponseField(IntField, desc = "数据总数")
    response.error_list = ResponseField(ListField, desc = '错误列表', fmt = CharField(desc = "错误列表"))

    @classmethod
    def get_desc(cls):
        return "手机设备导入数据接口"

    @classmethod
    def get_author(cls):
        return "Fsy"

    def execute(self, request):
        import_list, error_list = [], []
        for file_name, file_io in request._upload_files.items():
            # print(file_name, file_io.read())
            data_list, errors = import_mobile_devices_middleware.import_mobile_devices(file_io.read())
            import_list.extend(data_list)
            error_list.extend(errors)
        staff = self.auth_user
        record_detail = "{who} 在 {datetime} 进行了手机设备列表导入操作".format(who = staff.name,
                                                                      datetime = datetime.datetime.now().strftime(
                                                                          "%Y-%m-%d %H:%M:%S"))
        remark = "微信手机导入操作"
        JournalMiddleware.register(staff, OperationTypes.STAFF, staff, \
                                   OperationTypes.STAFF, JournalTypes.IMPORTDATA, record_detail, remark)
        return import_list, error_list

    def fill(self, response, import_list, error_list):
        response.total = len(import_list)
        response.error_list = error_list
        return response


class Search(StaffAuthorizedApi):
    """手机设备导入数据列表"""
    request = with_metaclass(RequestFieldSet)
    request.current_page = RequestField(IntField, desc = "当前查询页码")
    request.search_info = RequestField(DictField, desc = '搜索条件', conf = {
        'mobile_code': CharField(desc = "手机编号", is_required = False),
        'status': CharField(desc = "执行状态(初始化:init,执行中:excutting,已完成:finish,失败:failed)", is_required = False),
        'create_time_start': DatetimeField(desc = "上传开始时间", is_required = False),
        'create_time_end': DatetimeField(desc = "上传终止时间", is_required = False),
    })

    response = with_metaclass(ResponseFieldSet)
    response.data_list = ResponseField(ListField, desc = '手机设备导入数据列表', fmt = DictField(desc = "手机设备导入数据列表", conf = {
        'id': IntField(desc = "id"),
        'group_leader': CharField(desc = "组长姓名"),
        'mobile_code': CharField(desc = "手机编号"),
        'group_member': CharField(desc = "组员姓名"),
        'wechat_nick': CharField(desc = "微信昵称"),
        'wechat_number': CharField(desc = "微信号"),
        'wechat_password': CharField(desc = "微信密码"),
        'pay_password': CharField(desc = "微信支付密码"),
        'wechat_remark': CharField(desc = "微信号备注"),
        'department': CharField(desc = "部门"),
        'phone_number': CharField(desc = "手机号"),
        'operator': CharField(desc = "运营商"),
        'real_name': CharField(desc = "实名人姓名"),
        'phone_remark': CharField(desc = "手机号备注"),
        'flow_card_number': CharField(desc = "流量卡号"),
        'imei': CharField(desc = "手机imei号"),
        'brand': CharField(desc = "手机品牌"),
        'model': CharField(desc = "手机型号"),
        'price': IntField(desc = "购买价格/分"),
        'mobile_status': CharField(desc = "手机设备状态"),
        'mobile_remark': CharField(desc = "手机设备备注"),
        'phone_change': CharField(desc = "手机变更信息"),
        'status': CharField(desc = "状态"),
        'create_time': DatetimeField(desc = "创建时间"),
        'error_text': CharField(desc = "错误提示"),
    }))
    response.total = ResponseField(IntField, desc = "数据总数")
    response.total_page = ResponseField(IntField, desc = "总页码数")
    response.is_converting = ResponseField(BooleanField, desc = "是否正在转化")

    @classmethod
    def get_desc(cls):
        return "手机设备导入数据列表接口"

    @classmethod
    def get_author(cls):
        return "fsy"

    def execute(self, request):
        page_list = import_mobile_devices_middleware.search(request.current_page, **request.search_info)
        return page_list

    def fill(self, response, page_list):
        response.data_list = [{
            'id': mobile_devices.id,
            'group_leader': mobile_devices.group_leader,
            'mobile_code': mobile_devices.mobile_code,
            'group_member': mobile_devices.group_member,
            'wechat_nick': mobile_devices.wechat_nick,
            'wechat_number': mobile_devices.wechat_number,
            'wechat_password': mobile_devices.wechat_password,
            'pay_password': mobile_devices.pay_password,
            'wechat_remark': mobile_devices.wechat_remark,
            'department': mobile_devices.department,
            'phone_number': mobile_devices.phone_number,
            'operator': mobile_devices.operator,
            'real_name': mobile_devices.real_name,
            'phone_remark': mobile_devices.phone_remark,
            'flow_card_number': mobile_devices.flow_card_number,
            'imei': mobile_devices.imei,
            'brand': mobile_devices.brand,
            'model': mobile_devices.model,
            'price': mobile_devices.price,
            'mobile_status': mobile_devices.mobile_status,
            'mobile_remark': mobile_devices.mobile_remark,
            'phone_change': mobile_devices.phone_change,
            'status': mobile_devices.status,
            'create_time': mobile_devices.create_time,
            'error_text': mobile_devices.error_text,
        } for mobile_devices in page_list.data]
        response.total = page_list.total
        response.total_page = page_list.total_page
        response.is_converting = page_list.is_converting
        return response


class Convert(StaffAuthorizedApi):
    """手机设备导入数据转化"""
    request = with_metaclass(RequestFieldSet)
    request.search_info = RequestField(DictField, desc = '搜索条件', conf = {

    })

    response = with_metaclass(ResponseFieldSet)

    @classmethod
    def get_desc(cls):
        return "手机设备导入数据转化接口"

    @classmethod
    def get_author(cls):
        return "fsy"

    def execute(self, request):
        import_mobile_devices_middleware.exec_mobile_devices(**request.search_info)

    def fill(self, response):
        return response


class Update(StaffAuthorizedApi):
    """手机设备导入数据修改"""
    request = with_metaclass(RequestFieldSet)
    request.mobile_devices_id = RequestField(IntField, desc = '手机设备导入数据id')
    request.mobile_devices_info = RequestField(DictField, desc = "手机设备导入信息详情", conf = {
        'group_leader': CharField(desc = "组长姓名", is_required = False),
        'mobile_code': CharField(desc = "手机编号", is_required = False),
        'group_member': CharField(desc = "组员姓名", is_required = False),
        'wechat_nick': CharField(desc = "微信昵称", is_required = False),
        'wechat_number': CharField(desc = "微信号", is_required = False),
        'wechat_password': CharField(desc = "微信密码", is_required = False),
        'pay_password': CharField(desc = "微信支付密码", is_required = False),
        'wechat_remark': CharField(desc = "微信号备注", is_required = False),
        'department': CharField(desc = "部门", is_required = False),
        'phone_number': CharField(desc = "手机号", is_required = False),
        'operator': CharField(desc = "运营商", is_required = False),
        'real_name': CharField(desc = "实名人姓名", is_required = False),
        'phone_remark': CharField(desc = "手机号备注", is_required = False),
        'flow_card_number': CharField(desc = "流量卡号", is_required = False),
        'imei': CharField(desc = "手机imei号", is_required = False),
        'brand': CharField(desc = "手机品牌", is_required = False),
        'model': CharField(desc = "手机型号", is_required = False),
        'price': IntField(desc = "购买价格/分", is_required = False),
        'mobile_status': CharField(desc = "手机设备状态", is_required = False),
        'mobile_remark': CharField(desc = "手机设备备注", is_required = False),
        'phone_change': CharField(desc = "手机变更信息", is_required = False),
    })

    response = with_metaclass(ResponseFieldSet)

    @classmethod
    def get_desc(cls):
        return "手机设备导入数据修改接口"

    @classmethod
    def get_author(cls):
        return "fsy"

    def execute(self, request):
       import_mobile_devices_middleware.update(request.mobile_devices_id, **request.mobile_devices_info)

    def fill(self, response):
        return response

class ResetStatus(StaffAuthorizedApi):
    """手機設備数据狀態转化"""
    request = with_metaclass(RequestFieldSet)
    request.ids = RequestField(CharField, desc = '手機設備id列表', is_required = False)
    request.search_info = RequestField(DictField, desc = '搜索条件', conf = {
        'mobile_code': CharField(desc = "手机编号", is_required = False),
        'status': CharField(desc = "执行状态(初始化:init,执行中:excutting,已完成:finish,失败:failed)", is_required = False),
        'create_time_start': DatetimeField(desc = "上传开始时间", is_required = False),
        'create_time_end': DatetimeField(desc = "上传终止时间", is_required = False),
    })

    response = with_metaclass(ResponseFieldSet)

    @classmethod
    def get_desc(cls):
        return "手機設備狀態重置接口"

    @classmethod
    def get_author(cls):
        return "djd"

    def execute(self, request):
        if request.ids:
            id_list = json.loads(request.ids)
            request.search_info.update({'id__in': id_list})
        import_mobile_devices_middleware.reset_status(**request.search_info)
        staff = self.auth_user
        record_detail = "{who} 在 {datetime} 对ID为{id}的条目进行了状态重置操作".format(who = staff.name,
                                                                      datetime = datetime.datetime.now().strftime(
                                                                          "%Y-%m-%d %H:%M:%S"), id = id_list)
        remark = "导入手机設備状态重置初始化"
        JournalMiddleware.register(staff, OperationTypes.STAFF, staff, \
                                   OperationTypes.STAFF, JournalTypes.IMPORTRESET, record_detail, remark)

    def fill(self, response):
        return response
