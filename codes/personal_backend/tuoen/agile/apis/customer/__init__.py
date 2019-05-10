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
from tuoen.abs.service.customer.manager import CustomerServer
from tuoen.abs.service.mobile.manager import MobileDevicesServer


class Search(StaffAuthorizedApi):
    """客户列表"""
    request = with_metaclass(RequestFieldSet)
    request.current_page = RequestField(IntField, desc = "当前查询页码")
    request.search_info = RequestField(DictField, desc = '搜索条件', conf = {
        'name': CharField(desc = "客户姓名", is_required = False)
    })

    response = with_metaclass(ResponseFieldSet)
    response.data_list = ResponseField(ListField, desc = '客户列表', fmt = DictField(desc = "客户列表", conf = {
        'id': IntField(desc = "id"),
        'name': CharField(desc = "姓名"),
        'gender': CharField(desc = "性别"),
        'birthday': CharField(desc = "出身年月"),
        'email': CharField(desc = "邮箱"),
        'phone': CharField(desc = "手机号"),
        'wechat': CharField(desc = "微信号"),
        'city': CharField(desc = "城市"),
        'address': CharField(desc = "详细地址"),
        'mobilephone': CharField(desc = "设备编码"),
        'create_time': DatetimeField(desc = "进入时间"),
    }))
    response.total = ResponseField(IntField, desc = "数据总数")
    response.total_page = ResponseField(IntField, desc = "总页码数")

    @classmethod
    def get_desc(cls):
        return "客户列表接口"

    @classmethod
    def get_author(cls):
        return "fsy"

    def execute(self, request):
        page_list = CustomerServer.search(request.current_page, **request.search_info)
        # MobileDevicesServer.hung_devices_byphone(page_list.data)
        return page_list

    def fill(self, response, page_list):
        response.data_list = [{
                'id': customer.id,
                'name': customer.name,
                'gender': customer.gender,
                'birthday': customer.birthday,
                'email': customer.email,
                'phone': customer.phone,
                'wechat': customer.wechat,
                'city': customer.city,
                'address': customer.address,
                'mobilephone': customer.mobiledevices.code if customer.mobiledevices else "",
                'create_time': customer.create_time,
        } for customer in page_list.data]
        response.total = page_list.total
        response.total_page = page_list.total_page

        return response


class Get(StaffAuthorizedApi):
    """获取客户详情"""
    request = with_metaclass(RequestFieldSet)
    request.customer_id = RequestField(IntField, desc = '客户id')

    response = with_metaclass(ResponseFieldSet)
    response.customer_info = ResponseField(DictField, desc = "客户详情", conf = {
        'id': IntField(desc = "id"),
        'name': CharField(desc = "姓名"),
        'gender': CharField(desc = "性别"),
        'birthday': CharField(desc = "出身年月"),
        'email': CharField(desc = "邮箱"),
        'phone': CharField(desc = "手机号"),
        'wechat': CharField(desc = "微信号"),
        'city': CharField(desc = "城市"),
        'address': CharField(desc = "详细地址"),
        'mobilephone': CharField(desc = "设备编码"),
        'create_time': DatetimeField(desc = "进入时间"),
    })

    @classmethod
    def get_desc(cls):
        return "客户详情接口"

    @classmethod
    def get_author(cls):
        return "fsy"

    def execute(self, request):
        customer = CustomerServer.get(request.customer_id)
        # 挂载跟踪行为



        return customer

    def fill(self, response, customer):
        response.customer_info = {
                'id': customer.id,
                'name': customer.name,
                'gender': customer.gender,
                'birthday': customer.birthday,
                'email': customer.email,
                'phone': customer.phone,
                'wechat': customer.wechat,
                'city': customer.city,
                'address': customer.address,
                'mobilephone': customer.mobiledevices.code if customer.mobiledevices else "",
                'create_time': customer.create_time,
        }
        return response


class Update(StaffAuthorizedApi):
    """修改客户信息"""
    request = with_metaclass(RequestFieldSet)
    request.customer_id = RequestField(IntField, desc = '客户id')
    request.customer_info = RequestField(DictField, desc = "客户详情", conf = {
        'name': CharField(desc = "姓名", is_required = False),
        'gender': CharField(desc = "性别", is_required = False),
        'birthday': CharField(desc = "出身年月", is_required = False),
        'email': CharField(desc = "邮箱", is_required = False),
        'phone': CharField(desc = "手机号", is_required = False),
        'wechat': CharField(desc = "微信号", is_required = False),
        'nick': CharField(desc = "微信昵称", is_required = False),
        'city': CharField(desc = "城市", is_required = False),
        'address': CharField(desc = "详细地址", is_required = False),
    })

    response = with_metaclass(ResponseFieldSet)


    @classmethod
    def get_desc(cls):
        return "修改客户信息接口"

    @classmethod
    def get_author(cls):
        return "fsy"

    def execute(self, request):
        customer = CustomerServer.get(request.customer_id)
        CustomerServer.update(customer, **request.customer_info)
    def fill(self, response):
        return response
