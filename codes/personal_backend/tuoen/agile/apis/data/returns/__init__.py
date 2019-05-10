# coding=UTF-8

import json
from tuoen.sys.core.field.base import CharField, DictField, \
        IntField, ListField, DatetimeField, FileField, DateField, BooleanField
from tuoen.sys.core.api.utils import with_metaclass
from tuoen.sys.core.api.request import RequestField, RequestFieldSet
from tuoen.sys.core.api.response import ResponseField, ResponseFieldSet
from tuoen.sys.core.exception.business_error import BusinessError

from tuoen.agile.apis.base import StaffAuthorizedApi
from tuoen.abs.middleware.data import import_returns_middleware
import datetime
from model.store.model_journal import JournalTypes, OperationTypes
from tuoen.abs.middleware.journal import JournalMiddleware

class Upload(StaffAuthorizedApi):
    """退貨訂單数据导入接口"""
    request = with_metaclass(RequestFieldSet)
    request._upload_files = RequestField(FileField, desc = "上传文件")

    response = with_metaclass(ResponseFieldSet)
    response.total = ResponseField(IntField, desc = "数据总数")
    response.error_list = ResponseField(ListField, desc = '错误列表', fmt = CharField(desc = "错误列表"))

    @classmethod
    def get_desc(cls):
        return "退貨訂單数据导入接口"

    @classmethod
    def get_author(cls):
        return "djd"

    def execute(self, request):
        import_list, error_list = [], []
        for file_name, file_io in request._upload_files.items():
            data_list, errors = import_returns_middleware.import_returns(file_io.read())
            import_list.extend(data_list)
            error_list.extend(errors)
        return import_list, error_list

    def fill(self, response, import_list, error_list):
        response.total = len(import_list)
        response.error_list = error_list
        return response


class Search(StaffAuthorizedApi):
    """退貨訂單数据列表"""
    request = with_metaclass(RequestFieldSet)
    request.current_page = RequestField(IntField, desc = "当前查询页码")
    request.search_info = RequestField(DictField, desc = '搜索条件', conf = {
        # 'code': CharField(desc = "设备编码", is_required = False),
        'status': CharField(desc = "执行状态(初始化:init,执行中:excutting,已完成:finish,失败:failed)", is_required = False),
        'create_time_start': DatetimeField(desc = "上传开始时间", is_required = False),
        'create_time_end': DatetimeField(desc = "上传终止时间", is_required = False),
    })

    response = with_metaclass(ResponseFieldSet)
    response.data_list = ResponseField(ListField, desc = '退货订单数据列表', fmt = DictField(desc = "退貨訂單数据列表", conf = {
        'id': IntField(desc = "退貨單ID"),
        'status': CharField(desc = "执行状态"),
        'code': CharField(desc = "設備編碼"),
        'create_time': DatetimeField(desc = "创建时间"),
        'error_text': CharField(desc = "错误提示"),
    }))
    response.total = ResponseField(IntField, desc = "数据总数")
    response.total_page = ResponseField(IntField, desc = "总页码数")
    response.is_converting = ResponseField(BooleanField, desc = "是否正在转化")

    @classmethod
    def get_desc(cls):
        return "退貨訂單数据列表接口"

    @classmethod
    def get_author(cls):
        return "djd"

    def execute(self, request):
        page_list = import_returns_middleware.search(request.current_page, **request.search_info)
        return page_list

    def fill(self, response, page_list):
        response.data_list = [{
            'id': returns.id,
            'code': returns.code,
            'status': returns.status,
            'create_time': returns.create_time,
            'error_text': returns.error_text,
        } for returns in page_list.data]
        response.total = page_list.total
        response.total_page = page_list.total_page
        response.is_converting = page_list.is_converting
        return response


class Convert(StaffAuthorizedApi):
    """退貨訂單数据转化"""
    request = with_metaclass(RequestFieldSet)
    request.search_info = RequestField(DictField, desc = '搜索条件', conf = {

    })

    response = with_metaclass(ResponseFieldSet)

    @classmethod
    def get_desc(cls):
        return "退貨訂單数据转化接口"

    @classmethod
    def get_author(cls):
        return "djd"

    def execute(self, request):
        import_returns_middleware.exec_returns(**request.search_info)

    def fill(self, response):
        return response

class ResetStatus(StaffAuthorizedApi):
    """退貨訂單数据转化"""
    request = with_metaclass(RequestFieldSet)
    request.ids = RequestField(CharField, desc = '退貨id列表', is_required = False)
    request.search_info = RequestField(DictField, desc = '搜索条件', conf = {
        'status': CharField(desc = "执行状态(初始化:init,执行中:excutting,已完成:finish,失败:failed)", is_required = False),
        'create_time_start': DatetimeField(desc = "上传开始时间", is_required = False),
        'create_time_end': DatetimeField(desc = "上传终止时间", is_required = False),
    })

    response = with_metaclass(ResponseFieldSet)

    @classmethod
    def get_desc(cls):
        return "退貨訂單数据转化接口"

    @classmethod
    def get_author(cls):
        return "djd"

    def execute(self, request):
        if request.ids:
            id_list = json.loads(request.ids)
            request.search_info.update({'id__in': id_list})
        import_returns_middleware.reset_status(**request.search_info)
        staff = self.auth_user
        record_detail = "{who} 在 {datetime} 对ID为{id}的条目进行了状态重置操作".format(who = staff.name,
                                                                      datetime = datetime.datetime.now().strftime(
                                                                          "%Y-%m-%d %H:%M:%S"), id = id_list)
        remark = "导入退货订单状态重置初始化"
        JournalMiddleware.register(staff, OperationTypes.STAFF, staff, \
                                   OperationTypes.STAFF, JournalTypes.IMPORTRESET, record_detail, remark)
    def fill(self, response):
        return response
