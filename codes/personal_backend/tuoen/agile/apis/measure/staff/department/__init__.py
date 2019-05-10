# coding=UTF-8

# 环境的

# 第三方

# 公用的
from tuoen.sys.core.exception.business_error import BusinessError
from tuoen.sys.core.field.base import CharField, DictField, IntField, ListField, BooleanField, DatetimeField, DateField
from tuoen.sys.core.api.request import RequestField, RequestFieldSet
from tuoen.sys.core.api.utils import with_metaclass
from tuoen.sys.core.api.response import ResponseField, ResponseFieldSet

# 逻辑的  service | middleware - > apis
from tuoen.abs.middleware.department import department_middleware

from tuoen.agile.apis.base import NoAuthrizedApi, StaffAuthorizedApi
from tuoen.abs.service.user.manager import StaffServer
from tuoen.abs.service.measure.manager import MeasureStaffServer
from tuoen.abs.service.service.manager import ServiceItemServer
from tuoen.abs.service.permise.manager import StaffPermiseServer
from tuoen.abs.service.authority import UserRightServer
from tuoen.abs.service.order.manager import StaffOrderEventServer


class Search(StaffAuthorizedApi):
    """部门绩效列表"""
    request = with_metaclass(RequestFieldSet)
    request.current_page = RequestField(IntField, desc = "当前查询页码")
    request.search_info = RequestField(DictField, desc = '搜索条件', conf = {
        'staff_id': IntField(desc = "员工id", is_required = False),
        'department_id': IntField(desc = "部门", is_required = False),
        'begin_time': DateField(desc = "开始时间", is_required = False),
        'end_time': DateField(desc = "结束时间", is_required = False),
    })

    response = with_metaclass(ResponseFieldSet)
    response.sum_data = ResponseField(DictField, desc = "部门绩效统计", conf = {
        'new_number': IntField(desc = "当日新分数据"),
        'exhale_number': IntField(desc = "当日呼出数"),
        'call_number': IntField(desc = "当日接通数"),
        'wechat_number': IntField(desc = "添加微信数"),
        'call_rate': CharField(desc = "当日接通率"),
        'volume': IntField(desc = "当日成交量"),
        'conversion_rate': CharField(desc = "当日转化率"),
        'open_number': IntField(desc = "当日开通人数"),
        'open_rate': CharField(desc = "当日开通率"),
        'activation_number': IntField(desc = "当日激活人数"),
        'activation_rate': CharField(desc = "当日激活率"),
        'ysb_volume': IntField(desc="银收宝当日成交量"),
        'ysb_conversion_rate': CharField(desc="银收宝当日转化率"),
        'ysb_open_number': IntField(desc="银收宝当日开通人数"),
        'ysb_open_rate': CharField(desc="银收宝当日开通率"),
        'ysb_activation_number': IntField(desc="银收宝当日激活人数"),
        'ysb_activation_rate': CharField(desc="银收宝当日激活率"),
    })
    response.data_list = ResponseField(ListField, desc = '部门绩效列表', fmt = DictField(desc = "员工绩效列表", conf = {
        'id':IntField(desc = "绩效id"),
        'staff_id': IntField(desc = "员工id"),
        'staff_name': CharField(desc = "员工姓名"),
        'department_name': CharField(desc = "部门名称"),
        'record_id': IntField(desc = "记录人id"),
        'record_name': CharField(desc = "记录人姓名"),
        'new_number': IntField(desc = "当日新分数据"),
        'exhale_number': IntField(desc = "当日呼出数"),
        'call_number': IntField(desc = "当日接通数"),
        'call_rate': CharField(desc = "当日接通率"),
        'wechat_number': IntField(desc = "添加微信数"),
        'report_date': DateField(desc = "报表日期"),
        'create_time': DatetimeField(desc = "添加日期"),
        'remark': CharField(desc = "备注"),
        'volume': IntField(desc = "当日成交量"),
        'conversion_rate': CharField(desc = "当日转化率"),
        'open_number': IntField(desc = "当日开通人数"),
        'open_rate': CharField(desc = "当日开通率"),
        'activation_number': IntField(desc = "当日激活人数"),
        'activation_rate': CharField(desc = "当日激活率"),
        'ysb_volume': IntField(desc="银收宝当日成交量"),
        'ysb_conversion_rate': CharField(desc="银收宝当日转化率"),
        'ysb_open_number': IntField(desc="银收宝当日开通人数"),
        'ysb_open_rate': CharField(desc="银收宝当日开通率"),
        'ysb_activation_number': IntField(desc="银收宝当日激活人数"),
        'ysb_activation_rate': CharField(desc="银收宝当日激活率"),
    }))
    response.total = ResponseField(IntField, desc = "数据总数")
    response.total_page = ResponseField(IntField, desc = "总页码数")

    @classmethod
    def get_desc(cls):
        return "部门绩效列表接口"

    @classmethod
    def get_author(cls):
        return "fsy"

    def execute(self, request):
        if "staff_id" in request.search_info:
            staff_id = request.search_info.pop("staff_id")
            staff = StaffServer.get(staff_id)
            request.search_info.update({"staff":staff})
        cur_user = self.auth_user

        if "department_id" not in request.search_info:
            department_ids = StaffPermiseServer.get_staff_department_ids(cur_user)
            request.search_info.update({"department_id__in": department_ids})

        # user_pro = UserRightServer(cur_user)
        # request.search_info['cur_user'] = user_pro
        measure_staff_qs = MeasureStaffServer.search_qs(**request.search_info)
        sum_data = MeasureStaffServer.summing_new(**request.search_info)
        page_list = MeasureStaffServer.search(request.current_page, measure_staff_qs)
        MeasureStaffServer.calculation(page_list.data)

        if "department_id" in request.search_info:
            department_id = request.search_info.pop("department_id")
            department_ids = department_middleware.get_all_children_ids(department_id)
            department_ids.append(department_id)
        else:
            department_ids = request.search_info.pop("department_id__in")

        order_ids = StaffOrderEventServer.get_orders_bydepartmentids(department_ids)

        request.search_info.update({"order_id__in": order_ids})

        sum_measure_data = ServiceItemServer.summing(sum_data, **request.search_info)
        ServiceItemServer.huang_serviceitem_rate(page_list.data)
        if 'begin_time' in request.search_info:
            begin_time = request.search_info['begin_time']
        if 'end_time' in request.search_info:
            end_time = request.search_info['end_time']
        for ms in page_list.data:
            MeasureStaffServer.hung_ysb_measure_data(ms, begin_time, end_time)
        ysb_sum_measure_data = MeasureStaffServer.hung_ysb_total_rate(sum_data, **request.search_info)
        return sum_data, sum_measure_data, page_list, ysb_sum_measure_data

    def fill(self, response, sum_data, sum_measure_data, page_list, ysb_sum_measure_data):
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
        response.data_list = [{
            'id':measure_staff.id,
            'staff_id': measure_staff.staff.id if measure_staff.staff else 0,
            'staff_name': measure_staff.staff.name if measure_staff.staff else "",
            'department_name': measure_staff.department.name if measure_staff.department else "",
            'record_id': measure_staff.record.id if measure_staff.record else 0,
            'record_name': measure_staff.record.name if measure_staff.record else "",
            'new_number': measure_staff.new_number,
            'exhale_number': measure_staff.exhale_number,
            'call_number': measure_staff.call_number,
            'call_rate': measure_staff.call_rate,
            'wechat_number': measure_staff.wechat_number,
            'report_date': measure_staff.report_date,
            'create_time': measure_staff.create_time,
            'remark': measure_staff.remark,
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
    """员工绩效统计"""
    request = with_metaclass(RequestFieldSet)
    request.current_page = RequestField(IntField, desc = "当前查询页码")
    request.search_info = RequestField(DictField, desc = '搜索条件', conf = {

    })

    response = with_metaclass(ResponseFieldSet)
    response.data_list = ResponseField(ListField, desc = '员工绩效统计列表', fmt = DictField(desc = "员工绩效统计列表", conf = {
        'calculation_date': CharField(desc = "计算日期"),
        'new_number': IntField(desc = "当日新分数据"),
        'exhale_number': IntField(desc = "当日呼出数"),
        'call_number': IntField(desc = "当日接通数"),
        'call_rate': CharField(desc = "当日接通率"),
        'wechat_number': IntField(desc = "当日添加微信数"),
        'volume': IntField(desc = "当日成交量"),
        'conversion_rate': CharField(desc = "当日转化率"),
        'open_number': IntField(desc = "当日开通人数"),
        'open_rate': CharField(desc = "当日开通率"),
        'activation_number': IntField(desc = "当日激活人数"),
        'activation_rate': CharField(desc = "当日激活率"),
    }))

    @classmethod
    def get_desc(cls):
        return "员工绩效统计列表接口"

    @classmethod
    def get_author(cls):
        return "fsy"

    def execute(self, request):
        staff = self.auth_user
        staff_list = StaffPermiseServer.get_all_children_staff(staff)
        staff_list.append(staff)

    def fill(self, response, statistics_list):

        response.data_list = [{
            'calculation_date':item["calculation_date"],
            'new_number':item["new_number"],
            'exhale_number': item["exhale_number"],
            'call_number': item["call_number"],
            'call_rate': item["call_rate"],
            'wechat_number': item["wechat_number"],
            'volume': item["volume"],
            'conversion_rate': item["conversion_rate"],
            'open_number': item["open_number"],
            'open_rate': item["open_rate"],
            'activation_number': item["activation_number"],
            'activation_rate': item["activation_rate"]
        } for item in statistics_list]
        return response
