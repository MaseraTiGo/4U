# coding=UTF-8

import json
from tuoen.sys.core.field.base import CharField, DictField, \
        IntField, ListField, DatetimeField, FileField, DateField, BooleanField
from tuoen.sys.core.api.utils import with_metaclass
from tuoen.sys.core.api.request import RequestField, RequestFieldSet
from tuoen.sys.core.api.response import ResponseField, ResponseFieldSet
from tuoen.sys.core.exception.business_error import BusinessError

from tuoen.agile.apis.base import StaffAuthorizedApi
from tuoen.abs.middleware.data import import_staff_middleware
import datetime
from model.store.model_journal import JournalTypes, OperationTypes
from tuoen.abs.middleware.journal import JournalMiddleware

class Upload(StaffAuthorizedApi):
    """员工导入数据接口"""
    request = with_metaclass(RequestFieldSet)
    request._upload_files = RequestField(FileField, desc = "上传文件")

    response = with_metaclass(ResponseFieldSet)
    response.total = ResponseField(IntField, desc = "数据总数")
    response.error_list = ResponseField(ListField, desc = '错误列表', fmt = CharField(desc = "错误列表"))

    @classmethod
    def get_desc(cls):
        return "员工导入数据接口"

    @classmethod
    def get_author(cls):
        return "Fsy"

    def execute(self, request):
        import_list, error_list = [], []
        for file_name, file_io in request._upload_files.items():
            # print(file_name, file_io.read())
            data_list, errors = import_staff_middleware.import_staff(file_io.read())
            import_list.extend(data_list)
            error_list.extend(errors)
        return import_list, error_list

    def fill(self, response, import_list, error_list):
        response.total = len(import_list)
        response.error_list = error_list
        return response


class Search(StaffAuthorizedApi):
    """员工导入数据列表"""
    request = with_metaclass(RequestFieldSet)
    request.current_page = RequestField(IntField, desc = "当前查询页码")
    request.search_info = RequestField(DictField, desc = '搜索条件', conf = {
        'name': CharField(desc = "员工姓名", is_required = False),
        'status': CharField(desc = "执行状态(初始化:init,执行中:excutting,已完成:finish,失败:failed)", is_required = False),
        'create_time_start': DatetimeField(desc = "上传开始时间", is_required = False),
        'create_time_end': DatetimeField(desc = "上传终止时间", is_required = False),
    })

    response = with_metaclass(ResponseFieldSet)
    response.data_list = ResponseField(ListField, desc = '员工数据列表', fmt = DictField(desc = "员工数据列表", conf = {
        'id': IntField(desc = "id"),
        'name': CharField(desc = "姓名"),
        'position': CharField(desc = "职位"),
        'department': CharField(desc = "部门"),
        'phone': CharField(desc = "手机号"),
        'gender': CharField(desc = "性别"),
        'identity': CharField(desc = "身份证号"),
        'birthday': DateField(desc = "生日"),
        'age': IntField(desc = "年龄"),
        'emergency_contact': CharField(desc = "紧急联系人"),
        'emergency_phone': CharField(desc = "紧急联系人电话"),
        'address': CharField(desc = "详细地址"),
        'entry_time': DateField(desc = "入职时间"),
        'education': CharField(desc = "学历"),
        'bank_number': CharField(desc = "招行卡号"),
        'contract_b': CharField(desc = "合同编号（必）"),
        'contract_l': CharField(desc = "合同编号（立）"),
        'expire_time': DateField(desc = "到期时间"),
        'is_on_job': CharField(desc = "是否在职"),
        'quit_time': DateField(desc = "离职时间"),
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
        return "员工导入数据列表接口"

    @classmethod
    def get_author(cls):
        return "fsy"

    def execute(self, request):
        page_list = import_staff_middleware.search(request.current_page, **request.search_info)
        return page_list

    def fill(self, response, page_list):
        response.data_list = [{
            'id': staff.id,
            'name': staff.name,
            'position': staff.position,
            'department': staff.department,
            'phone': staff.phone,
            'gender': staff.gender,
            'identity': staff.identity,
            'birthday': staff.birthday,
            'age': staff.age,
            'emergency_contact': staff.emergency_contact,
            'emergency_phone': staff.emergency_phone,
            'address': staff.address,
            'entry_time': staff.entry_time,
            'education': staff.education,
            'bank_number': staff.bank_number,
            'contract_b': staff.contract_b,
            'contract_l': staff.contract_l,
            'expire_time': staff.expire_time,
            'is_on_job': staff.is_on_job,
            'quit_time': staff.quit_time,
            'status': staff.status,
            'remark': staff.remark,
            'create_time': staff.create_time,
            'error_text': staff.error_text,
        } for staff in page_list.data]
        response.total = page_list.total
        response.total_page = page_list.total_page
        response.is_converting = page_list.is_converting
        return response


class Convert(StaffAuthorizedApi):
    """员工数据数据转化"""
    request = with_metaclass(RequestFieldSet)
    request.search_info = RequestField(DictField, desc = '搜索条件', conf = {

    })

    response = with_metaclass(ResponseFieldSet)

    @classmethod
    def get_desc(cls):
        return "员工数据数据转化接口"

    @classmethod
    def get_author(cls):
        return "fsy"

    def execute(self, request):
        import_staff_middleware.exec_staff(**request.search_info)

    def fill(self, response):
        return response


class Update(StaffAuthorizedApi):
    """员工导入数据修改"""
    request = with_metaclass(RequestFieldSet)
    request.staff_id = RequestField(IntField, desc = '员工导入数据id')
    request.staff_info = RequestField(DictField, desc = "员工导入数据信息详情", conf = {
        'name': CharField(desc = "姓名", is_required = False),
        'position': CharField(desc = "职位", is_required = False),
        'department': CharField(desc = "部门", is_required = False),
        'phone': CharField(desc = "手机号", is_required = False),
        'gender': CharField(desc = "性别", is_required = False),
        'identity': CharField(desc = "身份证号", is_required = False),
        'birthday': DateField(desc = "生日", is_required = False),
        'age': IntField(desc = "年龄", is_required = False),
        'emergency_contact': CharField(desc = "紧急联系人", is_required = False),
        'emergency_phone': CharField(desc = "紧急联系人电话", is_required = False),
        'address': CharField(desc = "详细地址", is_required = False),
        'entry_time': DateField(desc = "入职时间", is_required = False),
        'education': CharField(desc = "学历", is_required = False),
        'bank_number': CharField(desc = "招行卡号", is_required = False),
        'contract_b': CharField(desc = "合同编号（必）", is_required = False),
        'contract_l': CharField(desc = "合同编号（立）", is_required = False),
        'expire_time': DateField(desc = "到期时间", is_required = False),
        'is_on_job': CharField(desc = "是否在职", is_required = False),
        'quit_time': DateField(desc = "离职时间", is_required = False),
        'remark': CharField(desc = "备注", is_required = False),
    })

    response = with_metaclass(ResponseFieldSet)

    @classmethod
    def get_desc(cls):
        return "员工导入数据修改接口"

    @classmethod
    def get_author(cls):
        return "fsy"

    def execute(self, request):
       import_staff_middleware.update(request.staff_id, **request.staff_info)

    def fill(self, response):
        return response

class ResetStatus(StaffAuthorizedApi):
    """員工數據狀態转化"""
    request = with_metaclass(RequestFieldSet)
    request.ids = RequestField(CharField, desc = '導入員工id列表', is_required = False)
    request.search_info = RequestField(DictField, desc = '搜索条件', conf = {
        'name': CharField(desc = "员工姓名", is_required = False),
        'status': CharField(desc = "执行状态(初始化:init,执行中:excutting,已完成:finish,失败:failed)", is_required = False),
        'create_time_start': DatetimeField(desc = "上传开始时间", is_required = False),
        'create_time_end': DatetimeField(desc = "上传终止时间", is_required = False),
    })

    response = with_metaclass(ResponseFieldSet)

    @classmethod
    def get_desc(cls):
        return "員工數據狀態重置接口"

    @classmethod
    def get_author(cls):
        return "djd"

    def execute(self, request):
        if request.ids:
            id_list = json.loads(request.ids)
            request.search_info.update({'id__in': id_list})
        import_staff_middleware.reset_status(**request.search_info)
        staff = self.auth_user
        record_detail = "{who} 在 {datetime} 对ID为{id}的条目进行了状态重置操作".format(who = staff.name,
                                                                      datetime = datetime.datetime.now().strftime(
                                                                          "%Y-%m-%d %H:%M:%S"), id = id_list)
        remark = "导入员工列表状态重置初始化"
        JournalMiddleware.register(staff, OperationTypes.STAFF, staff, \
                                   OperationTypes.STAFF, JournalTypes.IMPORTRESET, record_detail, remark)
    def fill(self, response):
        return response
