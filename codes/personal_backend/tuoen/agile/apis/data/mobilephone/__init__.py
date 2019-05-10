# coding=UTF-8

import json
from tuoen.sys.core.field.base import CharField, DictField, \
        IntField, ListField, DatetimeField, FileField, DateField, BooleanField
from tuoen.sys.core.api.utils import with_metaclass
from tuoen.sys.core.api.request import RequestField, RequestFieldSet
from tuoen.sys.core.api.response import ResponseField, ResponseFieldSet
from tuoen.sys.core.exception.business_error import BusinessError

from tuoen.agile.apis.base import StaffAuthorizedApi
from tuoen.abs.middleware.data import import_mobile_phone_middleware
import datetime
from model.store.model_journal import JournalTypes, OperationTypes
from tuoen.abs.middleware.journal import JournalMiddleware

class Upload(StaffAuthorizedApi):
    """手机号导入数据接口"""
    request = with_metaclass(RequestFieldSet)
    request._upload_files = RequestField(FileField, desc = "上传文件")

    response = with_metaclass(ResponseFieldSet)
    response.total = ResponseField(IntField, desc = "数据总数")
    response.error_list = ResponseField(ListField, desc = '错误列表', fmt = CharField(desc = "错误列表"))

    @classmethod
    def get_desc(cls):
        return "手机号导入数据接口"

    @classmethod
    def get_author(cls):
        return "Fsy"

    def execute(self, request):
        import_list, error_list = [], []
        for file_name, file_io in request._upload_files.items():
            # print(file_name, file_io.read())
            data_list, errors = import_mobile_phone_middleware.import_mobile_phone(file_io.read())
            import_list.extend(data_list)
            error_list.extend(errors)
        return import_list, error_list

    def fill(self, response, import_list, error_list):
        response.total = len(import_list)
        response.error_list = error_list
        return response


class Search(StaffAuthorizedApi):
    """手机号导入数据列表"""
    request = with_metaclass(RequestFieldSet)
    request.current_page = RequestField(IntField, desc = "当前查询页码")
    request.search_info = RequestField(DictField, desc = '搜索条件', conf = {
        'phone_number': CharField(desc = "手机号", is_required = False),
        'status': CharField(desc = "执行状态(初始化:init,执行中:excutting,已完成:finish,失败:failed)", is_required = False),
        'create_time_start': DatetimeField(desc = "上传开始时间", is_required = False),
        'create_time_end': DatetimeField(desc = "上传终止时间", is_required = False),
    })

    response = with_metaclass(ResponseFieldSet)
    response.data_list = ResponseField(ListField, desc = '手机设备导入数据列表', fmt = DictField(desc = "手机设备导入数据列表", conf = {
        'id': IntField(desc = "id"),
        'name': CharField(desc = "姓名"),
        'identity': CharField(desc = "身份证号"),
        'phone_number': CharField(desc = "手机号"),
        'department': CharField(desc = "部门"),
        'is_working': CharField(desc = "在职情况"),
        'card_password': CharField(desc = "手机卡密码"),
        'operator': CharField(desc = "运营商"),
        'rent': IntField(desc = "月租"),
        'phone_status': CharField(desc = "手机号状态"),
        'phone_remark': CharField(desc = "手机号备注"),
        'status': CharField(desc = "状态"),
        'create_time': DatetimeField(desc = "创建时间"),
        'error_text': CharField(desc = "错误提示"),
    }))
    response.total = ResponseField(IntField, desc = "数据总数")
    response.total_page = ResponseField(IntField, desc = "总页码数")
    response.is_converting = ResponseField(BooleanField, desc = "是否正在转化")

    @classmethod
    def get_desc(cls):
        return "手机号导入数据列表接口"

    @classmethod
    def get_author(cls):
        return "fsy"

    def execute(self, request):
        page_list = import_mobile_phone_middleware.search(request.current_page, **request.search_info)
        return page_list

    def fill(self, response, page_list):
        response.data_list = [{
            'id': mobile_phone.id,
            'name': mobile_phone.name,
            'identity': mobile_phone.identity,
            'phone_number': mobile_phone.phone_number,
            'department': mobile_phone.department,
            'is_working': mobile_phone.is_working,
            'card_password': mobile_phone.card_password,
            'operator': mobile_phone.operator,
            'rent': mobile_phone.rent,
            'phone_status': mobile_phone.phone_status,
            'phone_remark': mobile_phone.phone_remark,
            'status': mobile_phone.status,
            'create_time': mobile_phone.create_time,
            'error_text': mobile_phone.error_text,
        } for mobile_phone in page_list.data]
        response.total = page_list.total
        response.total_page = page_list.total_page
        response.is_converting = page_list.is_converting
        return response


class Convert(StaffAuthorizedApi):
    """手机号导入数据转化"""
    request = with_metaclass(RequestFieldSet)
    request.search_info = RequestField(DictField, desc = '搜索条件', conf = {

    })

    response = with_metaclass(ResponseFieldSet)

    @classmethod
    def get_desc(cls):
        return "手机号导入数据转化接口"

    @classmethod
    def get_author(cls):
        return "fsy"

    def execute(self, request):
        import_mobile_phone_middleware.exec_mobile_phone(**request.search_info)

    def fill(self, response):
        return response


class Update(StaffAuthorizedApi):
    """手机号导入数据修改"""
    request = with_metaclass(RequestFieldSet)
    request.mobile_phone_id = RequestField(IntField, desc = '手机号导入数据id')
    request.mobile_phone_info = RequestField(DictField, desc = "手机号信息详情", conf = {
        'name': CharField(desc = "姓名", is_required = False),
        'identity': CharField(desc = "身份证号", is_required = False),
        'phone_number': CharField(desc = "手机号", is_required = False),
        'department': CharField(desc = "部门", is_required = False),
        'is_working': CharField(desc = "在职情况", is_required = False),
        'card_password': CharField(desc = "手机卡密码", is_required = False),
        'operator': CharField(desc = "运营商", is_required = False),
        'rent': IntField(desc = "月租", is_required = False),
        'phone_status': CharField(desc = "手机号状态", is_required = False),
        'phone_remark': CharField(desc = "手机号备注", is_required = False),
    })

    response = with_metaclass(ResponseFieldSet)

    @classmethod
    def get_desc(cls):
        return "手机号导入数据修改接口"

    @classmethod
    def get_author(cls):
        return "fsy"

    def execute(self, request):
       import_mobile_phone_middleware.update(request.mobile_phone_id, **request.mobile_phone_info)

    def fill(self, response):
        return response

class ResetStatus(StaffAuthorizedApi):
    """手機数据狀態转化"""
    request = with_metaclass(RequestFieldSet)
    request.ids = RequestField(CharField, desc = '手機id列表', is_required = False)
    request.search_info = RequestField(DictField, desc = '搜索条件', conf = {
        'phone_number': CharField(desc = "手机号", is_required = False),
        'status': CharField(desc = "执行状态(初始化:init,执行中:excutting,已完成:finish,失败:failed)", is_required = False),
        'create_time_start': DatetimeField(desc = "上传开始时间", is_required = False),
        'create_time_end': DatetimeField(desc = "上传终止时间", is_required = False),
    })

    response = with_metaclass(ResponseFieldSet)

    @classmethod
    def get_desc(cls):
        return "手機狀態重置接口"

    @classmethod
    def get_author(cls):
        return "djd"

    def execute(self, request):
        if request.ids:
            id_list = json.loads(request.ids)
            request.search_info.update({'id__in': id_list})
        import_mobile_phone_middleware.reset_status(**request.search_info)
        staff = self.auth_user
        record_detail = "{who} 在 {datetime} 对ID为{id}的条目进行了状态重置操作".format(who = staff.name,
                                                                      datetime = datetime.datetime.now().strftime(
                                                                          "%Y-%m-%d %H:%M:%S"), id = id_list)
        remark = "导入手机號碼状态重置初始化"
        JournalMiddleware.register(staff, OperationTypes.STAFF, staff, \
                                   OperationTypes.STAFF, JournalTypes.IMPORTRESET, record_detail, remark)
    def fill(self, response):
        return response
