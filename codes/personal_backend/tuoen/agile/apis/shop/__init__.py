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
from tuoen.abs.service.shop.manager import ChannelServer, ShopServer


class Add(StaffAuthorizedApi):
    """添加店铺"""
    request = with_metaclass(RequestFieldSet)
    request.shop_info = RequestField(DictField, desc = "店铺详情", conf = {
        'name': CharField(desc = "店铺名称"),
        'freight': IntField(desc = "运费/分", is_required = False),
        'single_repair_money': IntField(desc = "单次补单金额/分", is_required = False),
        'single_point_money': IntField(desc = "单次扣点金额/分", is_required = False),
        'is_distribution': BooleanField(desc = "是否为分销店铺(0否，1是)", is_required = False, choices = [(0, "是"), (1, "否")]),
        'channel_id': IntField(desc = "店铺渠道id", is_required = False),
        'remark': CharField(desc = "备注", is_required = False),
    })

    response = with_metaclass(ResponseFieldSet)

    @classmethod
    def get_desc(cls):
        return "店铺添加接口"

    @classmethod
    def get_author(cls):
        return "fsy"

    def execute(self, request):
        ShopServer.is_name_exist(request.shop_info['name'])
        channel = ChannelServer.get(request.shop_info['channel_id'])
        request.shop_info.update({'channel': channel})
        ShopServer.generate(**request.shop_info)

    def fill(self, response):
        return response


class Search(StaffAuthorizedApi):
    """店铺列表"""
    request = with_metaclass(RequestFieldSet)
    request.current_page = RequestField(IntField, desc = "当前查询页码")
    request.search_info = RequestField(DictField, desc = '搜索条件', conf = {
        'name': CharField(desc = "关键字", is_required = False),
        'channel_id': IntField(desc = "店铺渠道id", is_required = False)
    })

    response = with_metaclass(ResponseFieldSet)
    response.data_list = ResponseField(ListField, desc = '店铺列表', fmt = DictField(desc = "店铺列表", conf = {
        'id': IntField(desc = "店铺id"),
        'name': CharField(desc = "店铺名称"),
        'freight': IntField(desc = "运费/分", is_required = False),
        'single_repair_money': IntField(desc = "单次补单金额/分"),
        'single_point_money': IntField(desc = "单次扣点金额/分"),
        'is_distribution': IntField(desc = "是否为分销店铺（0否，1是）"),
        'channel_id': CharField(desc = "渠道id"),
        'channel_name': CharField(desc = "渠道名称"),
        'remark': CharField(desc = "备注"),
        'update_time': DatetimeField(desc = "更新时间"),
        'create_time': DatetimeField(desc = "创建时间"),
    }))
    response.total = ResponseField(IntField, desc = "数据总数")
    response.total_page = ResponseField(IntField, desc = "总页码数")

    @classmethod
    def get_desc(cls):
        return "店铺列表接口"

    @classmethod
    def get_author(cls):
        return "fsy"

    def execute(self, request):
        shop_page = ShopServer.search(request.current_page, **request.search_info)

        return shop_page

    def fill(self, response, shop_page):
        response.data_list = [{
            'id': shop.id,
            'name': shop.name,
            'freight': shop.freight,
            'single_repair_money': shop.single_repair_money,
            'single_point_money': shop.single_point_money,
            'is_distribution': shop.is_distribution,
            'channel_id': shop.channel.id if shop.channel else "",
            'channel_name': shop.channel.name if shop.channel else "",
            'remark': shop.remark,
            'update_time': shop.update_time,
            'create_time': shop.create_time,
        } for shop in shop_page.data]
        response.total = shop_page.total
        response.total_page = shop_page.total_page
        return response


class SearchAll(StaffAuthorizedApi):
    """店铺列表"""
    request = with_metaclass(RequestFieldSet)
    request.search_info = RequestField(DictField, desc = '搜索条件', conf = {
        'channel_id': IntField(desc = "店铺渠道id", is_required = False)
    })

    response = with_metaclass(ResponseFieldSet)
    response.data_list = ResponseField(ListField, desc = '店铺列表', fmt = DictField(desc = "店铺列表", conf = {
        'id': IntField(desc = "店铺id"),
        'name': CharField(desc = "店铺名称"),
    }))

    @classmethod
    def get_desc(cls):
        return "搜索全部店铺列表接口"

    @classmethod
    def get_author(cls):
        return "fsy"

    def execute(self, request):
        if "channel_id" in request.search_info:
            channel = ChannelServer.get(request.search_info["channel_id"])
            request.search_info.update({"channel":channel})
        shop_list = ShopServer.search_all(**request.search_info)

        return shop_list

    def fill(self, response, shop_list):

        response.data_list = [{
            'id': shop.id,
            'name': shop.name,
        } for shop in shop_list]
        return response


class Get(StaffAuthorizedApi):
    """获取店铺详情"""
    request = with_metaclass(RequestFieldSet)
    request.shop_id = RequestField(IntField, desc = '店铺id')

    response = with_metaclass(ResponseFieldSet)
    response.shop_info = ResponseField(DictField, desc = "店铺详情", conf = {
        'id': IntField(desc = "店铺id"),
        'name': CharField(desc = "店铺名称"),
        'freight': IntField(desc = "运费/分"),
        'single_repair_money': IntField(desc = "单次补单金额/分"),
        'single_point_money': IntField(desc = "单次扣点金额/分"),
        'is_distribution': IntField(desc = "是否为分销店铺（0否，1是）"),
        'channel_name': CharField(desc = "渠道名称"),
        'remark': CharField(desc = "备注"),
        'update_time': DatetimeField(desc = "更新时间"),
        'create_time': DatetimeField(desc = "创建时间"),
    })

    @classmethod
    def get_desc(cls):
        return "店铺详情接口"

    @classmethod
    def get_author(cls):
        return "fsy"

    def execute(self, request):
        shop = ShopServer.get(request.shop_id)
        return shop

    def fill(self, response, shop):
        response.shop_info = {
            'id': shop.id,
            'name': shop.name,
            'single_repair_money': shop.single_repair_money,
            'single_point_money': shop.single_point_money,
            'is_distribution': shop.is_distribution,
            'channel_name': shop.channel.name,
            'remark': shop.remark,
            'update_time': shop.update_time,
            'create_time': shop.create_time,
        }
        return response


class Update(StaffAuthorizedApi):
    """修改店铺信息"""
    request = with_metaclass(RequestFieldSet)
    request.shop_id = RequestField(IntField, desc = '店铺id')
    request.shop_info = RequestField(DictField, desc = "店铺详情", conf = {
        'name': CharField(desc = "店铺名称"),
        'freight': IntField(desc = "运费/分", is_required = False),
        'channel_id': IntField(desc = "店铺渠道id", is_required = False),
        'single_repair_money': CharField(desc = "单次补单金额/分", is_required = False),
        'single_point_money': CharField(desc = "单次扣点金额/分", is_required = False),
        'is_distribution': BooleanField(desc = "是否为分销店铺(0否，1是)", is_required = False),
        'remark': CharField(desc = "备注", is_required = False),

    })

    response = with_metaclass(ResponseFieldSet)

    @classmethod
    def get_desc(cls):
        return "修改店铺接口"

    @classmethod
    def get_author(cls):
        return "fsy"

    def execute(self, request):
        shop = ShopServer.get(request.shop_id)
        ShopServer.is_name_exist(request.shop_info["name"], shop)

        if 'channel_id' in request.shop_info:
            channel = ChannelServer.get(request.shop_info['channel_id'])
            request.shop_info.update({'channel': channel})
        ShopServer.update(shop, **request.shop_info)
    def fill(self, response):
        return response


class Remove(StaffAuthorizedApi):
    """删除店铺"""
    request = with_metaclass(RequestFieldSet)
    request.shop_id = RequestField(IntField, desc = "店铺id")

    response = with_metaclass(ResponseFieldSet)

    @classmethod
    def get_desc(cls):
        return "店铺删除接口"

    @classmethod
    def get_author(cls):
        return "fsy"

    def execute(self, request):
        ShopServer.remove(request.shop_id)

    def fill(self, response):
        return response


class Match(StaffAuthorizedApi):
    request = with_metaclass(RequestFieldSet)
    request.keyword = RequestField(CharField, desc = "匹配信息(店铺名称)")
    request.size = RequestField(IntField, desc = "返回数量")

    response = with_metaclass(ResponseFieldSet)
    response.match_list = ResponseField(ListField, desc = '店铺列表', fmt = DictField(desc = "店铺列表", conf = {
        'id': IntField(desc = "店铺id"),
        'name': CharField(desc = "店铺名称"),
    }))

    @classmethod
    def get_desc(cls):
        return "通过店铺渠道名称匹配渠道基础信息"

    @classmethod
    def get_author(cls):
        return "Fsy"

    def execute(self, request):
        shop_list = ShopServer.match(request.keyword, request.size)
        return shop_list

    def fill(self, response, shop_list):
        response.match_list = [{
            'id': shop.id,
            'name': shop.name,
        } for shop in shop_list]
        return response
