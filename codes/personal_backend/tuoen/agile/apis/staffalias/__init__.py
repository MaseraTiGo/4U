# coding=UTF-8

# 环境的

# 第三方

# 公用的
from tuoen.sys.core.exception.business_error import BusinessError
from tuoen.sys.core.field.base import CharField, DictField, IntField, ListField, BooleanField, DatetimeField
from tuoen.sys.core.api.request import RequestField, RequestFieldSet
from tuoen.sys.core.api.utils import with_metaclass
from tuoen.sys.core.api.response import ResponseField, ResponseFieldSet

# 逻辑的  service | middleware - > apis
from tuoen.agile.apis.base import NoAuthrizedApi, StaffAuthorizedApi
from tuoen.abs.service.user.manager import StaffServer
from tuoen.abs.service.staffalias.manager import StaffAliasServer
from tuoen.abs.service.authority import UserRightServer

class Add(StaffAuthorizedApi):
    """添加员工别名"""
    request = with_metaclass(RequestFieldSet)
    request.alias_info = RequestField(DictField, desc = "别名", conf = {
        'staff_id': IntField(desc = "员工id"),
        'alias': CharField(desc = "员工别名"),
        'remark': CharField(desc = "备注", is_required = False),
    })

    response = with_metaclass(ResponseFieldSet)

    @classmethod
    def get_desc(cls):
        return "员工别名添加接口"

    @classmethod
    def get_author(cls):
        return "fsy"

    def execute(self, request):

        staff = StaffServer.get(request.alias_info["staff_id"])
        request.alias_info.update({"staff":staff})
        StaffAliasServer.is_name_exist(request.alias_info['alias'])
        # StaffServer.is_name_exist(request.alias_info['alias'])
        StaffAliasServer.generate(**request.alias_info)

    def fill(self, response):
        return response


class Search(StaffAuthorizedApi):
    """员工别名列表"""
    request = with_metaclass(RequestFieldSet)
    request.current_page = RequestField(IntField, desc = "当前查询页码")
    request.search_info = RequestField(DictField, desc = '搜索条件', conf = {
        'alias': CharField(desc = "员工别名", is_required = False)
    })

    response = with_metaclass(ResponseFieldSet)
    response.data_list = ResponseField(ListField, desc = '员工别名列表', fmt = DictField(desc = "员工别名列表", conf = {
        'id': IntField(desc = "id"),
        'staff_id': CharField(desc = "员工id"),
        'staff_name': CharField(desc = "员工姓名"),
        'alias': CharField(desc = "员工别名"),
        'gender': CharField(desc = "性别"),
        'number': CharField(desc = "工号"),
        'phone': CharField(desc = "手机号"),
        'identity': CharField(desc = "身份证号"),
        'remark': CharField(desc = "备注"),
        'create_time': DatetimeField(desc = "创建时间"),
    }))
    response.total = ResponseField(IntField, desc = "数据总数")
    response.total_page = ResponseField(IntField, desc = "总页码数")

    @classmethod
    def get_desc(cls):
        return "员工别名列表接口"

    @classmethod
    def get_author(cls):
        return "fsy"

    def execute(self, request):
        cur_user = self.auth_user
        user_pro = UserRightServer(cur_user)
        request.search_info.update({"staff_id__in": user_pro._staff_id_list})
        alias_page = StaffAliasServer.search(request.current_page, **request.search_info)

        return alias_page

    def fill(self, response, alias_page):
        response.data_list = [{
            'id': staff_alias.id,
            'staff_id': staff_alias.staff.id,
            'staff_name': staff_alias.staff.name,
            'alias': staff_alias.alias,
            'gender': staff_alias.staff.gender,
            'number': staff_alias.staff.number,
            'phone': staff_alias.staff.phone,
            'identity': staff_alias.staff.identity,
            'remark': staff_alias.remark,
            'create_time': staff_alias.create_time,
        } for staff_alias in alias_page.data]
        response.total = alias_page.total
        response.total_page = alias_page.total_page
        return response


class Update(StaffAuthorizedApi):
    """修改员工别名信息"""
    request = with_metaclass(RequestFieldSet)
    request.staff_alias_id = RequestField(IntField, desc = '员工别名id')
    request.alias_info = RequestField(DictField, desc = "别名信息", conf = {
        'alias': CharField(desc = "员工别名"),
        'remark': CharField(desc = "备注", is_required = False),
    })

    response = with_metaclass(ResponseFieldSet)

    @classmethod
    def get_desc(cls):
        return "修改员工别名接口"

    @classmethod
    def get_author(cls):
        return "fsy"

    def execute(self, request):
       staff_alias = StaffAliasServer.get(request.staff_alias_id)
       StaffAliasServer.is_name_exist(request.alias_info["alias"], staff_alias)
       # StaffServer.is_name_exist(request.alias_info['alias'])
       StaffAliasServer.update(staff_alias, **request.alias_info)

    def fill(self, response):
        return response


class Remove(StaffAuthorizedApi):
    """删除员工别名"""
    request = with_metaclass(RequestFieldSet)
    request.staff_alias_id = RequestField(IntField, desc = "员工别名id")

    response = with_metaclass(ResponseFieldSet)

    @classmethod
    def get_desc(cls):
        return "员工别名删除接口"

    @classmethod
    def get_author(cls):
        return "fsy"

    def execute(self, request):
        StaffAliasServer.remove(request.staff_alias_id)

    def fill(self, response):
        return response
