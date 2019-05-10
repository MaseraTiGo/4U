# coding=UTF-8

import json
from tuoen.sys.core.field.base import CharField, DictField, \
        IntField, ListField, DatetimeField, FileField, DateField, BooleanField
from tuoen.sys.core.api.utils import with_metaclass
from tuoen.sys.core.api.request import RequestField, RequestFieldSet
from tuoen.sys.core.api.response import ResponseField, ResponseFieldSet
from tuoen.sys.core.exception.business_error import BusinessError

from tuoen.agile.apis.base import StaffAuthorizedApi
from tuoen.abs.middleware.data import import_rebate_middleware
import datetime
from model.store.model_journal import JournalTypes, OperationTypes
from tuoen.abs.middleware.journal import JournalMiddleware

class Upload(StaffAuthorizedApi):
    """客户返利数据导入接口"""
    request = with_metaclass(RequestFieldSet)
    request._upload_files = RequestField(FileField, desc = "上传文件")

    response = with_metaclass(ResponseFieldSet)
    response.total = ResponseField(IntField, desc = "数据总数")
    response.error_list = ResponseField(ListField, desc = '错误列表', fmt = CharField(desc = "错误列表"))

    @classmethod
    def get_desc(cls):
        return "客户返利数据导入接口"

    @classmethod
    def get_author(cls):
        return "Fsy"

    def execute(self, request):
        import_list, error_list = [], []
        for file_name, file_io in request._upload_files.items():
            # print(file_name, file_io.read())
            data_list, errors = import_rebate_middleware.import_rebate(file_io.read())
            import_list.extend(data_list)
            error_list.extend(errors)
        return import_list, error_list

    def fill(self, response, import_list, error_list):
        response.total = len(import_list)
        response.error_list = error_list
        return response


class Search(StaffAuthorizedApi):
    """客户返利数据列表"""
    request = with_metaclass(RequestFieldSet)
    request.current_page = RequestField(IntField, desc = "当前查询页码")
    request.search_info = RequestField(DictField, desc = '搜索条件', conf = {
        'code': CharField(desc = "客户编码", is_required = False),
        'status': CharField(desc = "执行状态(初始化:init,执行中:excutting,已完成:finish,失败:failed)", is_required = False),
        'create_time_start': DatetimeField(desc = "上传开始时间", is_required = False),
        'create_time_end': DatetimeField(desc = "上传终止时间", is_required = False),
    })

    response = with_metaclass(ResponseFieldSet)
    response.data_list = ResponseField(ListField, desc = '客户返利数据列表', fmt = DictField(desc = "客户返利数据列表", conf = {
        'id': IntField(desc = "id"),
        'agent_id': CharField(desc = "代理商ID"),
        'agent_name': CharField(desc = "代理商名称"),
        'code': CharField(desc = "客户编码"),
        'name': CharField(desc = "客户名称"),
        'phone': CharField(desc = "注册手机号"),
        'activity_type': CharField(desc = "活动类型"),
        'device_code': CharField(desc = "设备编码"),
        'register_time': DatetimeField(desc = "注册时间"),
        'bind_time': DatetimeField(desc = "绑定时间"),
        'month': DateField(desc = "交易月份"),
        'transaction_amount': IntField(desc = "交易金额/分"),
        'effective_amount': IntField(desc = "有效金额/分"),
        'accumulate_amount': IntField(desc = "当月累计交易金额/分"),
        'history_amount': IntField(desc = "历史累计交易金额/分"),
        'type': CharField(desc = "号段类型"),
        'is_rebate': CharField(desc = "是否返利"),
        'status': CharField(desc = "状态"),
        'remark': CharField(desc = "备注"),
        'create_time': DatetimeField(desc = "创建时间"),
        'error_text': CharField(desc = "错误提示"),
    }))
    response.total = ResponseField(IntField, desc = "数据总数")
    response.total_page = ResponseField(IntField, desc = "总页码数")
    response.is_converting = ResponseField(BooleanField, desc = "是否正在转化")

    @classmethod
    def get_desc(cls):
        return "客户返利数据列表接口"

    @classmethod
    def get_author(cls):
        return "fsy"

    def execute(self, request):
        page_list = import_rebate_middleware.search(request.current_page, **request.search_info)
        return page_list

    def fill(self, response, page_list):
        response.data_list = [{
            'id': rebate.id,
            'agent_id': rebate.agent_id,
            'agent_name': rebate.agent_name,
            'code': rebate.code,
            'name': rebate.name,
            'phone': rebate.phone,
            'activity_type': rebate.activity_type,
            'device_code': rebate.device_code,
            'register_time': rebate.register_time,
            'bind_time': rebate.bind_time,
            'month': rebate.month,
            'transaction_amount': rebate.transaction_amount,
            'effective_amount': rebate.effective_amount,
            'accumulate_amount': rebate.accumulate_amount,
            'history_amount': rebate.history_amount,
            'type': rebate.type,
            'is_rebate': rebate.is_rebate,
            'status': rebate.status,
            'remark': rebate.remark,
            'create_time': rebate.create_time,
            'error_text': rebate.error_text,
        } for rebate in page_list.data]
        response.total = page_list.total
        response.total_page = page_list.total_page
        response.is_converting = page_list.is_converting
        return response


class Convert(StaffAuthorizedApi):
    """客户返利数据转化"""
    request = with_metaclass(RequestFieldSet)
    request.search_info = RequestField(DictField, desc = '搜索条件', conf = {

    })

    response = with_metaclass(ResponseFieldSet)

    @classmethod
    def get_desc(cls):
        return "客户返利数据转化接口"

    @classmethod
    def get_author(cls):
        return "fsy"

    def execute(self, request):
        import_rebate_middleware.exec_rebate(**request.search_info)

    def fill(self, response):
        return response

class ResetStatus(StaffAuthorizedApi):
    """返利導入數據狀態重置"""
    request = with_metaclass(RequestFieldSet)
    request.ids = RequestField(CharField, desc = '返利id列表', is_required = False)
    request.search_info = RequestField(DictField, desc = '搜索条件', conf = {
        'code': CharField(desc = "客户编码", is_required = False),
        'status': CharField(desc = "执行状态(初始化:init,执行中:excutting,已完成:finish,失败:failed)", is_required = False),
        'create_time_start': DatetimeField(desc = "上传开始时间", is_required = False),
        'create_time_end': DatetimeField(desc = "上传终止时间", is_required = False),
    })

    response = with_metaclass(ResponseFieldSet)

    @classmethod
    def get_desc(cls):
        return "返利狀態重置接口"

    @classmethod
    def get_author(cls):
        return "djd"

    def execute(self, request):
        if request.ids:
            id_list = json.loads(request.ids)
            request.search_info.update({'id__in': id_list})
        import_rebate_middleware.reset_status(**request.search_info)
        staff = self.auth_user
        record_detail = "{who} 在 {datetime} 对ID为{id}的条目进行了状态重置操作".format(who = staff.name,
                                                                      datetime = datetime.datetime.now().strftime(
                                                                          "%Y-%m-%d %H:%M:%S"), id = id_list)
        remark = "导入返利订单状态重置初始化"
        JournalMiddleware.register(staff, OperationTypes.STAFF, staff, \
                                   OperationTypes.STAFF, JournalTypes.IMPORTRESET, record_detail, remark)
    def fill(self, response):
        return response
