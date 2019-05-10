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
from tuoen.agile.apis.base import NoAuthrizedApi, StaffAuthorizedApi
from tuoen.abs.service.shop.manager import ShopServer
from tuoen.abs.service.measure.manager import MeasureShopServer
from tuoen.abs.service.shop.manager import ChannelServer

class Add(StaffAuthorizedApi):
    """添加店铺绩效"""
    request = with_metaclass(RequestFieldSet)
    request.report_info = RequestField(DictField, desc = "店铺绩效", conf = {
        'shop_id': IntField(desc = "店铺id"),
        'total_sales': IntField(desc = "销售总数"),
        'add_order_number': IntField(desc = "补单数量"),
        'through_number': IntField(desc = "直通车成交单数"),
        'through_money': IntField(desc = "直通车总花费/分"),
        'record_date': DateField(desc = "报表日期(Y-m-d)"),
        'remark': CharField(desc = "备注", is_required = False),
    })

    response = with_metaclass(ResponseFieldSet)

    @classmethod
    def get_desc(cls):
        return "店铺绩效添加接口"

    @classmethod
    def get_author(cls):
        return "fsy"

    def execute(self, request):
        staff = self.auth_user
        shop = ShopServer.get(request.report_info["shop_id"])

        check_info = {}
        check_info.update({'shop':shop, 'record_date':request.report_info["record_date"]})
        MeasureShopServer.check_repeat(None, **check_info)

        request.report_info.update({'shop': shop, 'staff':staff})
        MeasureShopServer.generate(**request.report_info)

    def fill(self, response):
        return response


class Search(StaffAuthorizedApi):
    """店铺绩效列表"""
    request = with_metaclass(RequestFieldSet)
    request.current_page = RequestField(IntField, desc = "当前查询页码")
    request.search_info = RequestField(DictField, desc = '搜索条件', conf = {
        'shop_name': CharField(desc = "店铺名称", is_required = False),
        'shop_channel_id': CharField(desc = "店铺渠道id", is_required = False),
        'begin_time': DateField(desc = "开始时间", is_required = False),
        'end_time': DateField(desc = "结束时间", is_required = False),
    })

    response = with_metaclass(ResponseFieldSet)
    response.sum_data = ResponseField(DictField, desc = "店铺绩效统计", conf = {
        'total_sales': IntField(desc = "销售总数"),
        'add_order_number': IntField(desc = "补单数量"),
        'add_order_total_money': IntField(desc = "补单费用/分"),
        'single_point_total_money': IntField(desc = "扣点费用/分"),
        'through_number': IntField(desc = "直通车成交单数"),
        'through_money': IntField(desc = "直通车总花费/分"),
        'total_freight': IntField(desc = "运费/分"),
        'total_spend': IntField(desc = "总推广花费/分"),
        'average_spend': IntField(desc = "平均推广花费/分"),
    })
    response.data_list = ResponseField(ListField, desc = '店铺绩效列表', fmt = DictField(desc = "店铺绩效列表", conf = {
        'id':IntField(desc = "报表id"),
        'shop_id': IntField(desc = "店铺id"),
        'shop_name': CharField(desc = "店铺名称"),
        'channel_id': IntField(desc = "店铺渠道id"),
        'channel_name': CharField(desc = "店铺渠道名称"),
        'staff_name':CharField(desc = "添加员工姓名"),
        'total_sales': IntField(desc = "销售总数"),
        'add_order_number': IntField(desc = "补单数量"),
        'add_order_total_money': IntField(desc = "补单费用/分"),
        'single_point_total_money': IntField(desc = "扣点费用/分"),
        'through_number': IntField(desc = "直通车成交单数"),
        'through_money': IntField(desc = "直通车总花费/分"),
        'total_freight': IntField(desc = "运费/分"),
        'record_date': DateField(desc = "报表日期"),
        'total_spend': IntField(desc = "总推广花费/分"),
        'average_spend': IntField(desc = "平均推广花费/分"),
        'remark': CharField(desc = "备注"),
    }))
    response.total = ResponseField(IntField, desc = "数据总数")
    response.total_page = ResponseField(IntField, desc = "总页码数")

    @classmethod
    def get_desc(cls):
        return "店铺绩效列表接口"

    @classmethod
    def get_author(cls):
        return "fsy"

    def execute(self, request):
        if "shop_name" in request.search_info:
            shop_name = request.search_info.pop("shop_name")
            shop_list = ShopServer.search_all(name = shop_name)
            request.search_info.update({"shop__in":shop_list})
        if "shop_channel_id" in request.search_info:
            shop_channel_id = request.search_info.pop("shop_channel_id")
            request.search_info.update({"shop__channel_id":shop_channel_id})
        measure_shop_qs = MeasureShopServer.search_qs(**request.search_info)
        sum_data = MeasureShopServer.summing_new(**request.search_info)
        measure_shop_page = MeasureShopServer.search(request.current_page, measure_shop_qs)
        measure_shop_page.data = ChannelServer.hung_channel_forshops(measure_shop_page.data)
        MeasureShopServer.calculation(measure_shop_page.data)
        return sum_data, measure_shop_page

    def fill(self, response, sum_data, measure_shop_page):
        response.sum_data = {
            'total_sales': sum_data.total_sales,
            'add_order_number': sum_data.add_order_number,
            'add_order_total_money': sum_data.add_order_total_money,
            'single_point_total_money': sum_data.single_point_total_money,
            'through_number': sum_data.through_number,
            'through_money': sum_data.through_money,
            'total_freight': sum_data.total_freight,
            'total_spend': sum_data.total_spend,
            'average_spend': sum_data.average_spend,
        }
        response.data_list = [{
            'id':report.id,
            'shop_id': report.shop.id,
            'shop_name': report.shop.name,
            'channel_id':report.channel.id if report.channel else 0,
            'channel_name':report.channel.name if report.channel else "",
            'staff_name':report.staff.name,
            'total_sales': report.total_sales,
            'add_order_number': report.add_order_number,
            'add_order_total_money': report.add_order_total_money,
            'single_point_total_money': report.single_point_total_money,
            'through_number': report.through_number,
            'through_money': report.through_money,
            'total_freight': report.total_freight,
            'record_date': report.record_date,
            'total_spend': report.total_spend,
            'average_spend': report.average_spend,
            'remark': report.remark,
        } for report in measure_shop_page.data]
        response.total = measure_shop_page.total
        response.total_page = measure_shop_page.total_page
        return response


class Get(StaffAuthorizedApi):
    """获取店铺绩效详情"""
    request = with_metaclass(RequestFieldSet)
    request.report_id = RequestField(IntField, desc = '店铺绩效id')

    response = with_metaclass(ResponseFieldSet)
    response.report_info = ResponseField(DictField, desc = "店铺绩效详情", conf = {
        'id':IntField(desc = "报表id"),
        'shop_id': IntField(desc = "店铺id"),
        'total_sales': IntField(desc = "销售总数"),
        'add_order_number': IntField(desc = "补单数量"),
        'through_number': IntField(desc = "直通车成交单数"),
        'through_money': IntField(desc = "直通车总花费/分"),
        'record_date': DateField(desc = "报表日期"),
        'remark': CharField(desc = "备注"),
    })

    @classmethod
    def get_desc(cls):
        return "店铺绩效详情接口"

    @classmethod
    def get_author(cls):
        return "fsy"

    def execute(self, request):
        report = MeasureShopServer.get(request.report_id)
        return report

    def fill(self, response, report):
        response.report_info = {
            'id': report.id,
            'shop_id': report.shop.id,
            'total_sales': report.total_sales,
            'add_order_number': report.add_order_number,
            'through_number': report.through_number,
            'through_money': report.through_money,
            'record_date': report.record_date,
            'remark': report.remark,
        }
        return response


class Update(StaffAuthorizedApi):
    """修改店铺绩效信息"""
    request = with_metaclass(RequestFieldSet)
    request.report_id = RequestField(IntField, desc = '店铺绩效id')
    request.report_info = RequestField(DictField, desc = "店铺绩效详情", conf = {
        'shop_id': IntField(desc = "店铺id"),
        'total_sales': IntField(desc = "销售总数"),
        'add_order_number': IntField(desc = "补单数量"),
        'through_number': IntField(desc = "直通车成交单数"),
        'through_money': IntField(desc = "直通车总花费/分"),
        'record_date': DateField(desc = "报表日期"),
        'remark': CharField(desc = "备注", is_required = False),
    })

    response = with_metaclass(ResponseFieldSet)

    @classmethod
    def get_desc(cls):
        return "修改店铺绩效接口"

    @classmethod
    def get_author(cls):
        return "fsy"

    def execute(self, request):
       measure_shop = MeasureShopServer.get(request.report_id)

       shop = ShopServer.get(request.report_info["shop_id"])

       check_info = {}
       check_info.update({'shop':shop, 'record_date':request.report_info["record_date"]})
       MeasureShopServer.check_repeat(measure_shop, **check_info)

       request.report_info.update({"shop":shop})
       MeasureShopServer.update(measure_shop, **request.report_info)

    def fill(self, response):
        return response


class Remove(StaffAuthorizedApi):
    """删除店铺绩效"""
    request = with_metaclass(RequestFieldSet)
    request.report_id = RequestField(IntField, desc = "店铺绩效id")

    response = with_metaclass(ResponseFieldSet)

    @classmethod
    def get_desc(cls):
        return "店铺绩效删除接口"

    @classmethod
    def get_author(cls):
        return "fsy"

    def execute(self, request):
        MeasureShopServer.remove(request.report_id)

    def fill(self, response):
        return response


class Statistics(StaffAuthorizedApi):
    """店铺绩效统计"""
    request = with_metaclass(RequestFieldSet)
    request.current_page = RequestField(IntField, desc = "当前查询页码")
    request.search_info = RequestField(DictField, desc = '搜索条件', conf = {

    })

    response = with_metaclass(ResponseFieldSet)
    response.data_list = ResponseField(ListField, desc = '员工列表', fmt = DictField(desc = "员工列表", conf = {
        'id': IntField(desc = "店铺id"),
        'name': CharField(desc = "店铺名称"),
        'channel_id': CharField(desc = "渠道id"),
        'channel_name': CharField(desc = "渠道名称"),
        'measure_shop_list': ListField(desc = '店铺绩效列表', fmt = DictField(desc = "店铺绩效列表", conf = {
            'record_date': CharField(desc = "报表日期(Y-m-d)"),
            'total_sales': IntField(desc = "销售总数"),
            'add_order_number': IntField(desc = "补单数量"),
            'add_order_money': IntField(desc = "补单费用/分"),
            'points': IntField(desc = "扣点费用/分"),
            'through_number': IntField(desc = "直通车成交单数"),
            'through_money': IntField(desc = "直通车总花费/分"),
            'freight': IntField(desc = "运费/分"),
            'total_spend': IntField(desc = "总推广花费/分"),
            'average_spend': IntField(desc = "平均推广花费/分"),
         })),
    }))
    response.total = ResponseField(IntField, desc = "数据总数")
    response.total_page = ResponseField(IntField, desc = "总页码数")

    @classmethod
    def get_desc(cls):
        return "店铺绩效接口"

    @classmethod
    def get_author(cls):
        return "fsy"

    def execute(self, request):
        shop_page = ShopServer.search(request.current_page, **request.search_info)
        shop_page.data = MeasureShopServer.hung_measure_forshops(shop_page.data)

        return shop_page

    def fill(self, response, shop_page):
        response.data_list = [{
            'id': shop.id,
            'name': shop.name,
            'channel_id': shop.channel.id if shop.channel else "",
            'channel_name': shop.channel.name if shop.channel else "",
            'measure_shop_list': [{
                            'record_date': key,
                            'total_sales': shop.measure_shop[key].total_sales,
                            'add_order_number': shop.measure_shop[key].add_order_number,
                            'add_order_money': shop.measure_shop[key].add_order_money,
                            'points': shop.measure_shop[key].points,
                            'through_number': shop.measure_shop[key].through_number,
                            'through_money': shop.measure_shop[key].through_money,
                            'freight': shop.measure_shop[key].freight,
                            'total_spend': shop.measure_shop[key].total_spend,
                            'average_spend': shop.measure_shop[key].average_spend
                           } for key in shop.measure_shop],
        } for shop in shop_page.data]
        response.total = shop_page.total
        response.total_page = shop_page.total_page
        return response
