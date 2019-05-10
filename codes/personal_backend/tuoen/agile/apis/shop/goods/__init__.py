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
from tuoen.abs.service.shop.manager import GoodsServer


class Search(StaffAuthorizedApi):
    """商品列表"""
    request = with_metaclass(RequestFieldSet)
    request.current_page = RequestField(IntField, desc = "当前查询页码")
    request.search_info = RequestField(DictField, desc = '搜索条件', conf = {
        'name': CharField(desc = "商品名称", is_required = False)
    })

    response = with_metaclass(ResponseFieldSet)
    response.data_list = ResponseField(ListField, desc = '商品列表', fmt = DictField(desc = "商品列表", conf = {
        'id': IntField(desc = "商品id"),
        'name': CharField(desc = "商品名称"),
        'alias': CharField(desc = "商品别名"),
        'code': CharField(desc = "商品编码"),
        'price': IntField(desc = "商品价格/分"),
        'rate': CharField(desc = "商品费率"),
        'introduction': CharField(desc = "商品简介"),
        'thumbnail': CharField(desc = "商品缩略图"),
        're_num': IntField(desc = "商品限购数量"),
        'shop_id': IntField(desc = "店铺id"),
        'shop_name': CharField(desc = "店铺名称"),
        'create_time': DatetimeField(desc = "创建时间"),
    }))
    response.total = ResponseField(IntField, desc = "数据总数")
    response.total_page = ResponseField(IntField, desc = "总页码数")

    @classmethod
    def get_desc(cls):
        return "商品列表接口"

    @classmethod
    def get_author(cls):
        return "fsy"

    def execute(self, request):
        goods_page = GoodsServer.search(request.current_page, **request.search_info)

        return goods_page

    def fill(self, response, goods_page):
        response.data_list = [{
            'id': goods.id,
            'name': goods.name,
            'alias': goods.alias,
            'code': goods.code,
            'price': goods.price,
            'rate': goods.rate,
            'introduction': goods.introduction,
            'thumbnail': goods.thumbnail,
            're_num': goods.re_num,
            'shop_id': goods.shop.id if goods.shop else "",
            'shop_name': goods.shop.name if goods.shop else "",
            'create_time': goods.create_time,
        } for goods in goods_page.data]
        response.total = goods_page.total
        response.total_page = goods_page.total_page
        return response


class SearchAll(StaffAuthorizedApi):
    """商品列表"""
    request = with_metaclass(RequestFieldSet)
    request.search_info = RequestField(DictField, desc = '搜索条件', conf = {

    })

    response = with_metaclass(ResponseFieldSet)
    response.data_list = ResponseField(ListField, desc = '商品列表', fmt = DictField(desc = "商品列表", conf = {
        'id': IntField(desc = "商品id"),
        'name': CharField(desc = "商品名称"),
        'alias': CharField(desc = "商品别名"),
        'code': CharField(desc = "商品编码"),
        'price': IntField(desc = "商品价格/分"),
        'rate': CharField(desc = "商品费率"),
        'introduction': CharField(desc = "商品简介"),
        'thumbnail': CharField(desc = "商品缩略图"),
        're_num': IntField(desc = "商品限购数量"),
        'shop_id': IntField(desc = "店铺id"),
        'shop_name': CharField(desc = "店铺名称"),
        'create_time': DatetimeField(desc = "创建时间"),
    }))

    @classmethod
    def get_desc(cls):
        return "搜索全部商品列表接口"

    @classmethod
    def get_author(cls):
        return "fsy"

    def execute(self, request):
        goods_list = GoodsServer.search_all()

        return goods_list

    def fill(self, response, goods_list):

        response.data_list = [{
            'id': goods.id,
            'name': goods.name,
            'alias': goods.alias,
            'code': goods.code,
            'price': goods.price,
            'rate': goods.rate,
            'introduction': goods.introduction,
            'thumbnail': goods.thumbnail,
            're_num': goods.re_num,
            'shop_id': goods.shop.id if goods.shop else "",
            'shop_name': goods.shop.name if goods.shop else "",
            'create_time': goods.create_time,
        } for goods in goods_list]
        return response


class Match(StaffAuthorizedApi):
    request = with_metaclass(RequestFieldSet)
    request.keyword = RequestField(CharField, desc = "匹配信息(商品名称)")
    request.size = RequestField(IntField, desc = "返回数量")

    response = with_metaclass(ResponseFieldSet)
    response.match_list = ResponseField(ListField, desc = '商品列表', fmt = DictField(desc = "商品列表", conf = {
        'id': IntField(desc = "商品id"),
        'name': CharField(desc = "商品名称"),
    }))

    @classmethod
    def get_desc(cls):
        return "通过商品名称匹配商品基础信息"

    @classmethod
    def get_author(cls):
        return "Fsy"

    def execute(self, request):
        goods_list = GoodsServer.match(request.keyword, request.size)
        return goods_list

    def fill(self, response, goods_list):
        response.match_list = [{
            'id': goods.id,
            'name': goods.name,
        } for goods in goods_list]
        return response
