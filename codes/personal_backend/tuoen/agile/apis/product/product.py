# coding=UTF-8

'''
Created on 2016年7月23日

@author: Administrator
'''

from tuoen.sys.core.field.base import CharField, DictField, IntField, ListField, DatetimeField, DateField, BooleanField
from tuoen.sys.core.api.utils import with_metaclass
from tuoen.sys.core.api.request import RequestField, RequestFieldSet
from tuoen.sys.core.api.response import ResponseField, ResponseFieldSet
from tuoen.sys.core.exception.business_error import BusinessError

from tuoen.agile.apis.base import StaffAuthorizedApi
from tuoen.abs.service.account.manager import StaffAccountServer
from tuoen.abs.service.user.manager import StaffServer
from tuoen.abs.service.permise.manager import StaffPermiseServer

from tuoen.abs.service.authority import UserRightServer
from tuoen.abs.service.product import ProductOperateServer

class Add(StaffAuthorizedApi):
    """添加产品"""
    request = with_metaclass(RequestFieldSet)
    request.product_info = RequestField(DictField, desc = "产品详情", conf = {
        'name': CharField(desc = "商品名称"),
        'alias': CharField(desc = "商品别名", is_required = False),
        'introduction': CharField(desc = "商品简介", is_required = False),
        'details': CharField(desc = "商品详情", is_required = False),
        'thumbnail': CharField(desc = "商品缩略图", is_required = False),
        'images': CharField(desc = "商品banner图", is_required = False),
        'postage': IntField(desc = "商品邮费/分", is_required = False),
        'rebate_money': IntField(desc = "返利金额/分", is_required = False),
        'p_type': CharField(desc = "类型", is_required = False),
        'code': CharField(desc = "编号", is_required = False),
        'provider': CharField(desc = "供应商", is_required = False),
    })

    response = with_metaclass(ResponseFieldSet)

    @classmethod
    def get_desc(cls):
        return "添加产品接口"

    @classmethod
    def get_author(cls):
        return "djd"

    def execute(self, request):
        """add executing"""
        ProductOperateServer.add(**request.product_info)
    def fill(self, response):
        return response

class Update(StaffAuthorizedApi):
    """修改产品详情"""
    request = with_metaclass(RequestFieldSet)
    request.product_info = RequestField(DictField, desc = "用户详情", conf = {
        'id': IntField(desc = "商品ID"),
        'name': CharField(desc = "商品名称", is_required = False),
        'alias': CharField(desc = "商品别名", is_required = False),
        'introduction': CharField(desc = "商品简介", is_required = False),
        'details': CharField(desc = "商品详情", is_required = False),
        'thumbnail': CharField(desc = "商品缩略图", is_required = False),
        'images': CharField(desc = "商品banner图", is_required = False),
        'postage': IntField(desc = "商品邮费/分", is_required = False),
        'rebate_money': IntField(desc = "返利金额/分", is_required = False),
        'p_type': CharField(desc = "类型", is_required = False),
        'code': CharField(desc = "编号", is_required = False),
        'provider': CharField(desc = "供应商", is_required = False),
    })

    response = with_metaclass(ResponseFieldSet)

    @classmethod
    def get_desc(cls):
        return "产品修改接口"

    @classmethod
    def get_author(cls):
        return "djd"

    def execute(self, request):
        ProductOperateServer.update(**request.product_info)

    def fill(self, response):
        return response

class Remove(StaffAuthorizedApi):
    """修改产品详情"""
    request = with_metaclass(RequestFieldSet)
    request.product_info = RequestField(DictField, desc = "用户详情", conf = {
        'id': IntField(desc = "商品ID"),
    })

    response = with_metaclass(ResponseFieldSet)

    @classmethod
    def get_desc(cls):
        return "产品删除接口"

    @classmethod
    def get_author(cls):
        return "djd"

    def execute(self, request):
        ProductOperateServer.remove(**request.product_info)

    def fill(self, response):
        return response

class Search(StaffAuthorizedApi):
    """产品搜索列表"""
    request = with_metaclass(RequestFieldSet)
    request.current_page = RequestField(IntField, desc = "当前查询页码")
    request.search_info = RequestField(DictField, desc = '搜索条件', conf = {
        'keyword': CharField(desc = "关键词", is_required = False),
    })

    response = with_metaclass(ResponseFieldSet)
    response.data_list = ResponseField(ListField, desc = '产品列表', fmt = DictField(desc = "产品列表", conf = {
        'id': IntField(desc="商品ID"),
        'name': CharField(desc="商品名称"),
        'alias': CharField(desc="商品别名", is_required=False),
        'introduction': CharField(desc="商品简介", is_required=False),
        'details': CharField(desc="商品详情", is_required=False),
        'thumbnail': CharField(desc="商品缩略图", is_required=False),
        'images': CharField(desc="商品banner图", is_required=False),
        'postage': IntField(desc="商品邮费/分", is_required=False),
        'rebate_money': IntField(desc="返利金额/分", is_required=False),
        'p_type': CharField(desc="类型", is_required=False),
        'code': CharField(desc="编号", is_required=False),
        'provider': CharField(desc="供应商", is_required=False),
    }))
    response.total = ResponseField(IntField, desc = "数据总数")
    response.total_page = ResponseField(IntField, desc = "总页码数")

    @classmethod
    def get_desc(cls):
        return "产品列表接口"

    @classmethod
    def get_author(cls):
        return "djd"

    def execute(self, request):
        product_pages = ProductOperateServer.search(request.current_page, **request.search_info)
        return product_pages

    def fill(self, response, product_pages):
        response.data_list = [{
            'id': product.id,
            'name': product.name,
            'alias': product.alias,
            'introduction': product.introduction,
            'details': product.details,
            'thumbnail': product.thumbnail,
            'images': product.images,
            'postage': product.postage,
            'rebate_money': product.rebate_money,
            'p_type': product.p_type,
            'code': product.code,
            'provider': product.provider,
        } for product in product_pages.data]
        response.total = product_pages.total
        response.total_page = product_pages.total_page
        return response
