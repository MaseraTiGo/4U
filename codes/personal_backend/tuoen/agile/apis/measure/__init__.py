# coding=UTF-8

# 环境的
import datetime
# 第三方

# 公用的
from tuoen.sys.core.exception.business_error import BusinessError
from tuoen.sys.core.field.base import CharField, DictField, IntField, ListField, BooleanField, DatetimeField, DateField
from tuoen.sys.core.api.request import RequestField, RequestFieldSet
from tuoen.sys.core.api.utils import with_metaclass
from tuoen.sys.core.api.response import ResponseField, ResponseFieldSet

# 逻辑的  service | middleware - > apis
from tuoen.agile.apis.base import NoAuthrizedApi, StaffAuthorizedApi
from tuoen.abs.service.permise.manager import StaffPermiseServer
from tuoen.abs.service.measure.manager import MeasureStaffServer
from tuoen.abs.service.service.manager import ServiceItemServer
from tuoen.abs.service.order.manager import OrderServer, StaffOrderEventServer
from tuoen.abs.service.authority import UserRightServer


class Statistics(StaffAuthorizedApi):
    """数据统计"""
    request = with_metaclass(RequestFieldSet)
    request.search_info = RequestField(DictField, desc = '搜索条件', conf = {
        'search_time': DateField(desc = "搜索时间", is_required = False),
    })

    response = with_metaclass(ResponseFieldSet)
    response.data_list = ResponseField(ListField, desc = '数据统计列表', fmt = DictField(desc = "数据统计统计列表", conf = {
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
        return "数据统计列表接口"

    @classmethod
    def get_author(cls):
        return "fsy"

    def execute(self, request):
        search_time = None
        cur_user = self.auth_user
        user_pro = UserRightServer(cur_user)
        if "search_time" in request.search_info:
            search_time = request.search_info.pop("search_time")

        search_info = {'search_time': search_time, 'cur_user': user_pro}
        measure_staff_mapping = MeasureStaffServer.Statistics(search_info)
        # staff_order_event_list = StaffOrderEventServer.get_event_bystaff(user_pro._staff_id_list)
        search_time = search_info['search_time']
        if search_time is None:
            current_time = datetime.datetime.now()
        else:
            current_time = search_time
        cur_date_first = datetime.datetime(current_time.year, current_time.month, 1)
        cur_date_last = datetime.datetime(current_time.year, current_time.month + 1, 1, 23, 59, 59) - datetime.timedelta(1)

        if user_pro._is_admin:
            service_item_list = ServiceItemServer.search_qs(order__pay_time__gte = cur_date_first, order__pay_time__lte = cur_date_last)
        else:
            department_ids = StaffPermiseServer.get_staff_department_ids(cur_user)
            order_ids = StaffOrderEventServer.get_orders_bydepartmentids(department_ids)
            service_item_list = ServiceItemServer.search_qs(order__pay_time__gte = cur_date_first, \
                                                            order__pay_time__lte = cur_date_last, \
                                                            service__seller_id__in = user_pro._staff_id_list, \
                                                            order__id__in = order_ids)

        statistics_list = ServiceItemServer.Statistics(measure_staff_mapping, service_item_list)
        return statistics_list

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
