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
from tuoen.abs.service.product import ProductModelServer

class Add(StaffAuthorizedApi):
    """添加产品"""
    request = with_metaclass(RequestFieldSet)
    request.product_model_info = RequestField(DictField, desc = "产品详情", conf = {
        'name': CharField(desc = "型号名称"),
        'rate': CharField(desc = "默认费率表", is_required = False),
        'remark': CharField(desc = "备注", is_required = False),
        'stock': CharField(desc = "商品库存", is_required = False),
        'product': IntField(desc = "产品ID"),
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
        ProductModelServer.add(**request.product_model_info)
    def fill(self, response):
        return response

class Update(StaffAuthorizedApi):
    """修改产品型号详情"""
    request = with_metaclass(RequestFieldSet)
    request.product_info = RequestField(DictField, desc = "用户详情", conf = {
        'id': IntField(desc="型号ID"),
        'name': CharField(desc="型号名称", is_required=False),
        'rate': CharField(desc="默认费率表", is_required=False),
        'remark': CharField(desc="备注", is_required=False),
        'stock': CharField(desc="商品库存", is_required=False),
        'product': IntField(desc="产品ID", is_required=False),
    })

    response = with_metaclass(ResponseFieldSet)

    @classmethod
    def get_desc(cls):
        return "产品型号修改接口"

    @classmethod
    def get_author(cls):
        return "djd"

    def execute(self, request):
        ProductModelServer.update(**request.product_info)

    def fill(self, response):
        return response

class Remove(StaffAuthorizedApi):
    """修改产品详情"""
    request = with_metaclass(RequestFieldSet)
    request.product_info = RequestField(DictField, desc = "用户详情", conf = {
        'id': IntField(desc="型号ID"),
    })

    response = with_metaclass(ResponseFieldSet)

    @classmethod
    def get_desc(cls):
        return "产品型号删除接口"

    @classmethod
    def get_author(cls):
        return "djd"

    def execute(self, request):
        ProductModelServer.remove(**request.product_info)

    def fill(self, response):
        return response

class Search(StaffAuthorizedApi):
    """产品搜索列表"""
    request = with_metaclass(RequestFieldSet)
    #request.current_page = RequestField(IntField, desc = "当前查询页码")
    request.search_info = RequestField(DictField, desc = '搜索条件', conf = {
        'id': CharField(desc = "产品id", is_required = False),
    })

    response = with_metaclass(ResponseFieldSet)
    response.data_list = ResponseField(ListField, desc = '产品列表', fmt = DictField(desc = "产品列表", conf = {
        'id': IntField(desc = "产品型号Id"),
        'name': CharField(desc = "型号名称"),
        'rate': CharField(desc = "默认费率表", is_required = False),
        'remark': CharField(desc = "备注", is_required = False),
        'stock': CharField(desc = "商品库存", is_required = False),
        'create_time': DatetimeField(desc = "创建时间", is_required = False),
    }))
    #response.total = ResponseField(IntField, desc = "数据总数")
    #response.total_page = ResponseField(IntField, desc = "总页码数")

    @classmethod
    def get_desc(cls):
        return "产品列表接口"

    @classmethod
    def get_author(cls):
        return "djd"

    def execute(self, request):
        #product_model_pages = ProductModelServer.search(request.current_page, **request.search_info)
        product_model_list = ProductModelServer.search(**request.search_info)
        return product_model_list

    def fill(self, response, product_model_list):
        response.data_list = [{
            'id': product.id,
            'name': product.name,
            'rate': product.rate,
            'remark': product.remark,
            'stock': product.stock,
            'create_time': product.create_time,
        } for product in product_model_list]
        #response.total = product_model_pages.total
        #response.total_page = product_model_pages.total_page
        return response
