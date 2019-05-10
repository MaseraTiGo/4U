# coding=UTF-8

# 环境的

# 第三方

# 逻辑的  service | middleware - > apis
from tuoen.abs.middleware.department import department_middleware
from tuoen.abs.service.measure.manager import MeasureStaffServer
from tuoen.abs.service.order.manager import StaffOrderEventServer
from tuoen.abs.service.permise.manager import StaffPermiseServer
from tuoen.abs.service.user.manager import StaffServer
from tuoen.agile.apis.base import StaffAuthorizedApi
from tuoen.sys.core.api.request import RequestField, RequestFieldSet
from tuoen.sys.core.api.response import ResponseField, ResponseFieldSet
from tuoen.sys.core.api.utils import with_metaclass
# 公用的
from tuoen.sys.core.field.base import CharField, DictField, IntField, ListField, DatetimeField, BooleanField


class Search(StaffAuthorizedApi):
    """员工绩效统计列表"""
    request = with_metaclass(RequestFieldSet)
    request.current_page = RequestField(IntField, desc="当前查询页码")
    request.search_info = RequestField(DictField, desc='搜索条件', conf={
        'staff_id': IntField(desc="员工id", is_required=False),
        'department_id': IntField(desc="部门", is_required=False),
        'begin_time': DatetimeField(desc="开始时间", is_required=False),
        'end_time': DatetimeField(desc="结束时间", is_required=False),
        'new_protect': BooleanField(desc="是否保护", is_required=False),
    })

    response = with_metaclass(ResponseFieldSet)
    response.data_list = ResponseField(ListField, desc='部门绩效列表', fmt=DictField(desc="员工绩效列表", conf={
        'id': IntField(desc="员工ID"),
        'staff_name': CharField(desc="员工姓名"),
        'department_name': CharField(desc="部门名称"),
        'new_number': IntField(desc="当月新分数据"),
        'exhale_number': IntField(desc="当月呼出数"),
        'call_number': IntField(desc="当月接通数"),
        'call_rate': CharField(desc="当月接通率"),
        'wechat_number': IntField(desc="添加微信数"),
        'volume': IntField(desc="当月成交量"),
        'conversion_rate': CharField(desc="当月转化率"),
        'open_number': IntField(desc="当月开通人数"),
        'open_rate': CharField(desc="当月开通率"),
        'activation_number': IntField(desc="当月激活人数"),
        'activation_rate': CharField(desc="当月激活率"),
        'ysb_volume': IntField(desc="银收宝当月成交量"),
        'ysb_conversion_rate': CharField(desc="银收宝当月转化率"),
        'ysb_open_number': IntField(desc="银收宝当月开通人数"),
        'ysb_open_rate': CharField(desc="银收宝当月开通率"),
        'ysb_activation_number': IntField(desc="银收宝当月激活人数"),
        'ysb_activation_rate': CharField(desc="银收宝当月激活率"),
        'new_protect': BooleanField(desc="新人保护")
    }))
    response.total = ResponseField(IntField, desc="数据总数")
    response.total_page = ResponseField(IntField, desc="总页码数")

    @classmethod
    def get_desc(cls):
        return "绩效员工统计列表接口"

    @classmethod
    def get_author(cls):
        return "djd"

    def execute(self, request):
        if "staff_id" in request.search_info:
            staff_id = request.search_info.pop("staff_id")
            staff = StaffServer.get(staff_id)
            request.search_info.update({"staff": staff})
        cur_user = self.auth_user

        if "department_id" not in request.search_info:
            department_ids = StaffPermiseServer.get_staff_department_ids(cur_user)
            request.search_info.update({"department_id__in": department_ids})
        page_list = MeasureStaffServer.staff_sum_list(request.current_page, **request.search_info)
        return page_list

    def fill(self, response, page_list):
        response.data_list = [{
            'id': measure_staff.staff_id,
            'new_protect': measure_staff.new_protect,
            'staff_name': measure_staff.staff_name,
            'department_name': measure_staff.department,
            'new_number': measure_staff.new_number,
            'exhale_number': measure_staff.exhale_number,
            'call_number': measure_staff.call_number,
            'call_rate': measure_staff.call_rate,
            'wechat_number': measure_staff.wechat_number,
            'volume': measure_staff.volume,
            'conversion_rate': measure_staff.conversion_rate,
            'open_number': measure_staff.open_number,
            'open_rate': measure_staff.open_rate,
            'activation_number': measure_staff.activation_number,
            'activation_rate': measure_staff.activation_rate,
            'ysb_volume': measure_staff.ysb_volume,
            'ysb_conversion_rate': measure_staff.ysb_conversion_rate,
            'ysb_open_number': measure_staff.ysb_open_number,
            'ysb_open_rate': measure_staff.ysb_open_rate,
            'ysb_activation_number': measure_staff.ysb_activation_number,
            'ysb_activation_rate': measure_staff.ysb_activation_rate,
        } for measure_staff in page_list.data]
        response.total = page_list.total
        response.total_page = page_list.total_page
        return response


class Statistics(StaffAuthorizedApi):
    """绩效统计列表"""
    request = with_metaclass(RequestFieldSet)
    request.search_info = RequestField(DictField, desc='搜索条件', conf={
        'staff_id': IntField(desc="员工id", is_required=False),
        'department_id': IntField(desc="部门", is_required=False),
        'begin_time': DatetimeField(desc="开始时间", is_required=False),
        'end_time': DatetimeField(desc="结束时间", is_required=False),
        'new_protect': BooleanField(desc="是否保护", is_required=False),
    })

    response = with_metaclass(ResponseFieldSet)
    response.sum_data = ResponseField(DictField, desc="部门绩效统计", conf={
        'new_number': IntField(desc="当月新分数据"),
        'exhale_number': IntField(desc="当月呼出数"),
        'call_number': IntField(desc="当月接通数"),
        'wechat_number': IntField(desc="添加微信数"),
        'call_rate': CharField(desc="当月接通率"),
        'volume': IntField(desc="当月成交量"),
        'conversion_rate': CharField(desc="当月转化率"),
        'open_number': IntField(desc="当月开通人数"),
        'open_rate': CharField(desc="当月开通率"),
        'activation_number': IntField(desc="当月激活人数"),
        'activation_rate': CharField(desc="当月激活率"),
        'ysb_volume': IntField(desc="银收宝当月成交量"),
        'ysb_conversion_rate': CharField(desc="银收宝当月转化率"),
        'ysb_open_number': IntField(desc="银收宝当月开通人数"),
        'ysb_open_rate': CharField(desc="银收宝当月开通率"),
        'ysb_activation_number': IntField(desc="银收宝当月激活人数"),
        'ysb_activation_rate': CharField(desc="银收宝当月激活率"),
    })

    @classmethod
    def get_desc(cls):
        return "绩效总计列表接口"

    @classmethod
    def get_author(cls):
        return "djd"

    def execute(self, request):
        if 'new_protect' in request.search_info:
            request.search_info.pop('new_protect')
        if "staff_id" in request.search_info:
            staff_id = request.search_info.pop("staff_id")
            staff = StaffServer.get(staff_id)
            request.search_info.update({"staff": staff})
        cur_user = self.auth_user

        if "department_id" not in request.search_info:
            department_ids = StaffPermiseServer.get_staff_department_ids(cur_user)
            request.search_info.update({"department_id__in": department_ids})

        sum_data = MeasureStaffServer.total_calculate(**request.search_info)

        if "department_id" in request.search_info:
            department_id = request.search_info.pop("department_id")
            department_ids = department_middleware.get_all_children_ids(department_id)
            department_ids.append(department_id)
        else:
            department_ids = request.search_info.pop("department_id__in")

        order_ids = StaffOrderEventServer.get_orders_bydepartmentids(department_ids)

        request.search_info.update({"order_id__in": order_ids})

        sum_measure_data = MeasureStaffServer.hung_total_rate(sum_data, **request.search_info)
        ysb_sum_measure_data = MeasureStaffServer.hung_ysb_total_rate(sum_data, **request.search_info)
        return sum_data, sum_measure_data, ysb_sum_measure_data

    def fill(self, response, sum_data, sum_measure_data, ysb_sum_measure_data):
        response.sum_data = {
            'new_number': sum_data.new_number,
            'exhale_number': sum_data.exhale_number,
            'call_number': sum_data.call_number,
            'wechat_number': sum_data.wechat_number,
            'call_rate': sum_data.call_rate,
            'volume': sum_measure_data.volume_total,
            'conversion_rate': sum_measure_data.conversion_rate_total,
            'open_number': sum_measure_data.open_number_total,
            'open_rate': sum_measure_data.open_rate_total,
            'activation_number': sum_measure_data.activation_number_total,
            'activation_rate': sum_measure_data.activation_rate_total,
            'ysb_volume': ysb_sum_measure_data.volume_total,
            'ysb_conversion_rate': ysb_sum_measure_data.conversion_rate_total,
            'ysb_open_number': ysb_sum_measure_data.open_number_total,
            'ysb_open_rate': ysb_sum_measure_data.open_rate_total,
            'ysb_activation_number': ysb_sum_measure_data.activation_number_total,
            'ysb_activation_rate': ysb_sum_measure_data.activation_rate_total,
        }
        return response


class ExportData(StaffAuthorizedApi):
    """绩效统计列表"""
    request = with_metaclass(RequestFieldSet)
    request.search_info = RequestField(DictField, desc='搜索条件', conf={
        'staff_id': IntField(desc="员工id", is_required=False),
        'department_id': IntField(desc="部门", is_required=False),
        'begin_time': DatetimeField(desc="开始时间", is_required=False),
        'end_time': DatetimeField(desc="结束时间", is_required=False),
        'new_protect': BooleanField(desc="是否保护", is_required=False),
    })

    response = with_metaclass(ResponseFieldSet)
    response.data_list = ResponseField(ListField, desc='部门绩效列表', fmt=DictField(desc="员工绩效列表", conf={
        'id': IntField(desc="员工ID"),
        'staff_name': CharField(desc="员工姓名"),
        'department_name': CharField(desc="部门名称"),
        'new_number': IntField(desc="当月新分数据"),
        'exhale_number': IntField(desc="当月呼出数"),
        'call_number': IntField(desc="当月接通数"),
        'call_rate': CharField(desc="当月接通率"),
        'wechat_number': IntField(desc="添加微信数"),
        'volume': IntField(desc="当月成交量"),
        'conversion_rate': CharField(desc="当月转化率"),
        'open_number': IntField(desc="当月开通人数"),
        'open_rate': CharField(desc="当月开通率"),
        'activation_number': IntField(desc="当月激活人数"),
        'activation_rate': CharField(desc="当月激活率"),
        'new_protect': BooleanField(desc="新人保护")
    }))

    @classmethod
    def get_desc(cls):
        return "绩效员工统计列表接口"

    @classmethod
    def get_author(cls):
        return "djd"

    def execute(self, request):
        if "staff_id" in request.search_info:
            staff_id = request.search_info.pop("staff_id")
            staff = StaffServer.get(staff_id)
            request.search_info.update({"staff": staff})
        cur_user = self.auth_user

        if "department_id" not in request.search_info:
            department_ids = StaffPermiseServer.get_staff_department_ids(cur_user)
            request.search_info.update({"department_id__in": department_ids})
        current_page = 'useless'
        data_obj_list = MeasureStaffServer.staff_sum_list(current_page, is_split=False, **request.search_info)
        return data_obj_list

    def fill(self, response, data_obj_list):
        response.data_list = [{
            'id': measure_staff.staff_id,
            'new_protect': measure_staff.new_protect,
            'staff_name': measure_staff.staff_name,
            'department_name': measure_staff.department,
            'new_number': measure_staff.new_number,
            'exhale_number': measure_staff.exhale_number,
            'call_number': measure_staff.call_number,
            'call_rate': measure_staff.call_rate,
            'wechat_number': measure_staff.wechat_number,
            'volume': measure_staff.volume,
            'conversion_rate': measure_staff.conversion_rate,
            'open_number': measure_staff.open_number,
            'open_rate': measure_staff.open_rate,
            'activation_number': measure_staff.activation_number,
            'activation_rate': measure_staff.activation_rate,
        } for measure_staff in data_obj_list]
        return response
