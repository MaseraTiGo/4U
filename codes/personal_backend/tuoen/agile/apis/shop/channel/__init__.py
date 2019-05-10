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
    """添加店铺渠道"""
    request = with_metaclass(RequestFieldSet)
    request.channel_info = RequestField(DictField, desc = "渠道详情", conf = {
        'name': CharField(desc = "渠道名称", is_required = False),
        'freight': IntField(desc = "运费/分", is_required = False),
        'single_repair_money': IntField(desc = "单次补单金额/分", is_required = False),
        'single_point_money': IntField(desc = "单次扣点金额/分", is_required = False),
        'remark': CharField(desc = "备注", is_required = False),
    })

    response = with_metaclass(ResponseFieldSet)

    @classmethod
    def get_desc(cls):
        return "店铺渠道添加接口"

    @classmethod
    def get_author(cls):
        return "fsy"

    def execute(self, request):

        ChannelServer.is_name_exist(request.channel_info['name'])
        ChannelServer.generate(**request.channel_info)

    def fill(self, response):
        return response


class Search(StaffAuthorizedApi):
    """店铺渠道列表"""
    request = with_metaclass(RequestFieldSet)
    request.current_page = RequestField(IntField, desc = "当前查询页码")
    request.search_info = RequestField(DictField, desc = '搜索条件', conf = {
        'name': CharField(desc = "店铺渠道名称", is_required = False)
    })

    response = with_metaclass(ResponseFieldSet)
    response.data_list = ResponseField(ListField, desc = '店铺渠道列表', fmt = DictField(desc = "店铺渠道列表", conf = {
        'id': IntField(desc = "店铺渠道id"),
        'name': CharField(desc = "店铺渠道名称"),
        'shop_num': IntField(desc = "店铺数目"),
        'freight': IntField(desc = "运费/分"),
        'single_repair_money': IntField(desc = "单次补单金额/分"),
        'single_point_money': IntField(desc = "单次扣点金额/分"),
        'remark': CharField(desc = "备注"),
        'update_time': DatetimeField(desc = "更新时间"),
        'create_time': DatetimeField(desc = "创建时间"),
    }))
    response.total = ResponseField(IntField, desc = "数据总数")
    response.total_page = ResponseField(IntField, desc = "总页码数")

    @classmethod
    def get_desc(cls):
        return "店铺渠道列表接口"

    @classmethod
    def get_author(cls):
        return "fsy"

    def execute(self, request):
        channel_page = ChannelServer.search(request.current_page, **request.search_info)
        # 挂载店铺数量
        ShopServer.hung_shopnum_bychannel(channel_page.data)
        return channel_page

    def fill(self, response, channel_page):
        response.data_list = [{
            'id': channel.id,
            'name': channel.name,
            'shop_num': channel.shop_num,
            'freight': channel.freight,
            'single_repair_money': channel.single_repair_money,
            'single_point_money': channel.single_point_money,
            'remark': channel.remark,
            'update_time': channel.update_time,
            'create_time': channel.create_time,
        } for channel in channel_page.data]
        response.total = channel_page.total
        response.total_page = channel_page.total_page
        return response


class SearchAll(StaffAuthorizedApi):
    """店铺渠道列表"""
    request = with_metaclass(RequestFieldSet)
    request.search_info = RequestField(DictField, desc = '搜索条件', conf = {

    })

    response = with_metaclass(ResponseFieldSet)
    response.data_list = ResponseField(ListField, desc = '店铺渠道列表', fmt = DictField(desc = "店铺渠道列表", conf = {
        'id': IntField(desc = "店铺渠道id"),
        'name': CharField(desc = "店铺渠道名称"),
        'freight': IntField(desc = "运费/分"),
        'single_repair_money': IntField(desc = "单次补单金额/分"),
        'single_point_money': IntField(desc = "单次扣点金额/分"),
    }))

    @classmethod
    def get_desc(cls):
        return "搜索全部店铺渠道列表接口"

    @classmethod
    def get_author(cls):
        return "fsy"

    def execute(self, request):
        channel_list = ChannelServer.search_all(**request.search_info)

        return channel_list

    def fill(self, response, channel_list):

        response.data_list = [{
            'id': channel.id,
            'name': channel.name,
            'freight': channel.freight,
            'single_repair_money': channel.single_repair_money,
            'single_point_money': channel.single_point_money,
        } for channel in channel_list]
        return response


class Get(StaffAuthorizedApi):
    """获取店铺渠道详情"""
    request = with_metaclass(RequestFieldSet)
    request.channel_id = RequestField(IntField, desc = '店铺渠道id')

    response = with_metaclass(ResponseFieldSet)
    response.channel_info = ResponseField(DictField, desc = "店铺渠道详情", conf = {
        'id': IntField(desc = "店铺渠道id"),
        'name': CharField(desc = "店铺渠道名称"),
        'freight': IntField(desc = "运费/分"),
        'single_repair_money': IntField(desc = "单次补单金额/分"),
        'single_point_money': IntField(desc = "单次扣点金额/分"),
        'remark': CharField(desc = "备注"),
        'update_time': DatetimeField(desc = "更新时间"),
        'create_time': DatetimeField(desc = "创建时间"),
    })

    @classmethod
    def get_desc(cls):
        return "店铺渠道详情接口"

    @classmethod
    def get_author(cls):
        return "fsy"

    def execute(self, request):
        channel = ChannelServer.get(request.channel_id)
        return channel

    def fill(self, response, channel):
        response.channel_info = {
            'id': channel.id,
            'name': channel.name,
            'single_repair_money': channel.single_repair_money,
            'single_point_money': channel.single_point_money,
            'remark': channel.remark,
            'update_time': channel.update_time,
            'create_time': channel.create_time,
        }
        return response


class Update(StaffAuthorizedApi):
    """修改店铺渠道信息"""
    request = with_metaclass(RequestFieldSet)
    request.channel_id = RequestField(IntField, desc = '店铺渠道id')
    request.channel_info = RequestField(DictField, desc = "店铺渠道详情", conf = {
        'name': CharField(desc = "店铺渠道名称", is_required = False),
        'freight': IntField(desc = "运费/分", is_required = False),
        'single_repair_money': CharField(desc = "单次补单金额/分", is_required = False),
        'single_point_money': CharField(desc = "单次扣点金额/分", is_required = False),
        'remark': CharField(desc = "备注", is_required = False),

    })

    response = with_metaclass(ResponseFieldSet)

    @classmethod
    def get_desc(cls):
        return "修改店铺渠道接口"

    @classmethod
    def get_author(cls):
        return "fsy"

    def execute(self, request):
       channel = ChannelServer.get(request.channel_id)
       ChannelServer.is_name_exist(request.channel_info['name'], channel)
       ChannelServer.update(channel, **request.channel_info)

    def fill(self, response):
        return response


class Remove(StaffAuthorizedApi):
    """删除店铺渠道"""
    request = with_metaclass(RequestFieldSet)
    request.channel_id = RequestField(IntField, desc = "店铺渠道id")

    response = with_metaclass(ResponseFieldSet)

    @classmethod
    def get_desc(cls):
        return "店铺渠道删除接口"

    @classmethod
    def get_author(cls):
        return "fsy"

    def execute(self, request):
        ChannelServer.remove(request.channel_id)

    def fill(self, response):
        return response


class Match(StaffAuthorizedApi):
    request = with_metaclass(RequestFieldSet)
    request.keyword = RequestField(CharField, desc = "匹配信息(店铺渠道名称)")
    request.size = RequestField(IntField, desc = "返回数量")

    response = with_metaclass(ResponseFieldSet)
    response.match_list = ResponseField(ListField, desc = '店铺渠道列表', fmt = DictField(desc = "店铺渠道列表", conf = {
        'id': IntField(desc = "店铺渠道id"),
        'name': CharField(desc = "店铺渠道名称"),
        'single_repair_money': IntField(desc = "单次补单金额/分"),
        'single_point_money': IntField(desc = "单次扣点金额/分"),
    }))

    @classmethod
    def get_desc(cls):
        return "通过店铺渠道名称匹配渠道基础信息"

    @classmethod
    def get_author(cls):
        return "Fsy"

    def execute(self, request):
        channel_list = ChannelServer.match(request.keyword, request.size)
        return channel_list

    def fill(self, response, channel_list):
        response.match_list = [{
            'id': channel.id,
            'name': channel.name,
            'single_repair_money': channel.name,
            'single_point_money': channel.name,
        } for channel in channel_list]
        return response
