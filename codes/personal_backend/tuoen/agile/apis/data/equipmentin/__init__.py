# coding=UTF-8

import json
from tuoen.sys.core.field.base import CharField, DictField, \
        IntField, ListField, DatetimeField, FileField, DateField, BooleanField
from tuoen.sys.core.api.utils import with_metaclass
from tuoen.sys.core.api.request import RequestField, RequestFieldSet
from tuoen.sys.core.api.response import ResponseField, ResponseFieldSet
from tuoen.sys.core.exception.business_error import BusinessError

from tuoen.agile.apis.base import StaffAuthorizedApi
from tuoen.abs.middleware.data import import_equipment_in_middleware
import datetime
from model.store.model_journal import JournalTypes, OperationTypes
from tuoen.abs.middleware.journal import JournalMiddleware

class Upload(StaffAuthorizedApi):
    """设备入库数据导入接口"""
    request = with_metaclass(RequestFieldSet)
    request._upload_files = RequestField(FileField, desc = "上传文件")

    response = with_metaclass(ResponseFieldSet)
    response.total = ResponseField(IntField, desc = "数据总数")
    response.error_list = ResponseField(ListField, desc = '错误列表', fmt = CharField(desc = "错误列表"))

    @classmethod
    def get_desc(cls):
        return "设备入库数据导入接口"

    @classmethod
    def get_author(cls):
        return "Fsy"

    def execute(self, request):
        import_list, error_list = [], []
        for file_name, file_io in request._upload_files.items():
            # print(file_name, file_io.read())
            data_list, errors = import_equipment_in_middleware.import_equipment_in(file_io.read())
            import_list.extend(data_list)
            error_list.extend(errors)
        return import_list, error_list

    def fill(self, response, import_list, error_list):
        response.total = len(import_list)
        response.error_list = error_list
        return response


class Search(StaffAuthorizedApi):
    """设备入库数据列表"""
    request = with_metaclass(RequestFieldSet)
    request.current_page = RequestField(IntField, desc = "当前查询页码")
    request.search_info = RequestField(DictField, desc = '搜索条件', conf = {
        'add_time': DateField(desc = "添加日期", is_required = False),
        'status': CharField(desc = "执行状态(初始化:init,执行中:excutting,已完成:finish,失败:failed)", is_required = False),
        'create_time_start': DatetimeField(desc = "上传开始时间", is_required = False),
        'create_time_end': DatetimeField(desc = "上传终止时间", is_required = False),
    })

    response = with_metaclass(ResponseFieldSet)
    response.data_list = ResponseField(ListField, desc = '客户返利数据列表', fmt = DictField(desc = "客户返利数据列表", conf = {
        'id': IntField(desc = "id"),
        'add_time': CharField(desc = "添加时间"),
        'agent_name': CharField(desc = "代理商名称"),
        'product_type': CharField(desc = "产品类型"),
        'product_model': CharField(desc = "产品型号"),
        'min_number': CharField(desc = "起始号段"),
        'max_number': CharField(desc = "终止号段"),
        'quantity': IntField(desc = "入库数量"),
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
        return "设备入库数据列表接口"

    @classmethod
    def get_author(cls):
        return "fsy"

    def execute(self, request):
        page_list = import_equipment_in_middleware.search(request.current_page, **request.search_info)
        return page_list

    def fill(self, response, page_list):
        response.data_list = [{
            'id': equipmentin.id,
            'add_time': equipmentin.add_time,
            'agent_name': equipmentin.agent_name,
            'product_type': equipmentin.product_type,
            'product_model': equipmentin.product_model,
            'min_number': equipmentin.min_number,
            'max_number': equipmentin.max_number,
            'quantity': equipmentin.quantity,
            'status': equipmentin.status,
            'remark': equipmentin.remark,
            'create_time': equipmentin.create_time,
            'error_text': equipmentin.error_text
        } for equipmentin in page_list.data]
        response.total = page_list.total
        response.total_page = page_list.total_page
        response.is_converting = page_list.is_converting
        return response


class Convert(StaffAuthorizedApi):
    """设备入库数据转化"""
    request = with_metaclass(RequestFieldSet)
    request.search_info = RequestField(DictField, desc = '搜索条件', conf = {

    })

    response = with_metaclass(ResponseFieldSet)

    @classmethod
    def get_desc(cls):
        return "设备入库数据转化接口"

    @classmethod
    def get_author(cls):
        return "fsy"

    def execute(self, request):
        import_equipment_in_middleware.exec_equipment_in(**request.search_info)

    def fill(self, response):
        return response


class Update(StaffAuthorizedApi):
    """设备入库数据修改"""
    request = with_metaclass(RequestFieldSet)
    request.equipment_in_id = RequestField(IntField, desc = '设备入库信息id')
    request.equipment_in_info = RequestField(DictField, desc = "设备入库信息详情", conf = {
        'min_number': IntField(desc = "起始号段", is_required = False),
        'max_number': IntField(desc = "终止号段", is_required = False),
    })

    response = with_metaclass(ResponseFieldSet)

    @classmethod
    def get_desc(cls):
        return "设备入库数据修改接口"

    @classmethod
    def get_author(cls):
        return "fsy"

    def execute(self, request):
       import_equipment_in_middleware.update(request.equipment_in_id, **request.equipment_in_info)

    def fill(self, response):
        return response

class ResetStatus(StaffAuthorizedApi):
    """入庫設備数据狀態转化"""
    request = with_metaclass(RequestFieldSet)
    request.ids = RequestField(CharField, desc = '入庫設備id列表', is_required = False)
    request.search_info = RequestField(DictField, desc = '搜索条件', conf = {
        'add_time': DateField(desc = "添加日期", is_required = False),
        'status': CharField(desc = "执行状态(初始化:init,执行中:excutting,已完成:finish,失败:failed)", is_required = False),
        'create_time_start': DatetimeField(desc = "上传开始时间", is_required = False),
        'create_time_end': DatetimeField(desc = "上传终止时间", is_required = False),
    })

    response = with_metaclass(ResponseFieldSet)

    @classmethod
    def get_desc(cls):
        return "入庫設備狀態重置接口"

    @classmethod
    def get_author(cls):
        return "djd_"

    def execute(self, request):
        if request.ids:
            id_list = json.loads(request.ids)
            request.search_info.update({'id__in': id_list})
        import_equipment_in_middleware.reset_status(**request.search_info)
        staff = self.auth_user
        record_detail = "{who} 在 {datetime} 对ID为{id}的条目进行了状态重置操作".format(who = staff.name,
                                                                      datetime = datetime.datetime.now().strftime(
                                                                          "%Y-%m-%d %H:%M:%S"), id = id_list)
        remark = "导入设备入库状态重置初始化"
        JournalMiddleware.register(staff, OperationTypes.STAFF, staff, \
                                   OperationTypes.STAFF, JournalTypes.IMPORTRESET, record_detail, remark)

    def fill(self, response):
        return response
