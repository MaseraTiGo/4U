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
from tuoen.abs.service.user.manager import StaffServer
from tuoen.abs.service.customer.manager import SaleChanceServer
from tuoen.abs.service.shop.manager import GoodsServer
from tuoen.abs.service.authority import UserRightServer

class Add(StaffAuthorizedApi):
    """添加销售机会"""
    request = with_metaclass(RequestFieldSet)
    request.sale_chance_info = RequestField(DictField, desc = "添加销售机会", conf = {
        'customer_ids': ListField(desc = '客户ids', fmt = IntField(desc = '客户id')),
        'staff_id': IntField(desc = "员工id"),
        'goods_id': IntField(desc = "商品id"),
        'end_time': DateField(desc = "截至时间"),
    })

    response = with_metaclass(ResponseFieldSet)

    @classmethod
    def get_desc(cls):
        return "添加销售机会接口"

    @classmethod
    def get_author(cls):
        return "fsy"

    def execute(self, request):
        staff = StaffServer.get(request.sale_chance_info["staff_id"])
        goods = GoodsServer.get(request.sale_chance_info["goods_id"])
        customer_list = CustomerServer.search_qs(id__in = request.sale_chance_info["customer_ids"])
        for customer in customer_list:
            SaleChanceServer.generate(customer = customer, staff = staff, goods = goods, shop = goods.shop, \
                                      end_time = request.sale_chance_info["end_time"])


    def fill(self, response):
        return response


class Search(StaffAuthorizedApi):
    """销售机会列表"""
    request = with_metaclass(RequestFieldSet)
    request.current_page = RequestField(IntField, desc = "当前查询页码")
    request.search_info = RequestField(DictField, desc = '搜索条件', conf = {
        'name': CharField(desc = "客户姓名", is_required = False)
    })

    response = with_metaclass(ResponseFieldSet)
    response.data_list = ResponseField(ListField, desc = '销售机会', fmt = DictField(desc = "销售机会", conf = {
        'id': IntField(desc = "机会id"),
        'staff_id': IntField(desc = "员工id"),
        'staff_name': CharField(desc = "员工姓名"),
        'customer_id': IntField(desc = "客户id"),
        'name': CharField(desc = "姓名"),
        'gender': CharField(desc = "性别"),
        'birthday': DatetimeField(desc = "出身年月"),
        'email': CharField(desc = "邮箱"),
        'phone': CharField(desc = "手机号"),
        'wechat': CharField(desc = "微信号"),
        'city': CharField(desc = "城市"),
        'address': CharField(desc = "详细地址"),
        'good_name': CharField(desc = "偏好商品名称"),
        'good_id': CharField(desc = "偏好商品id"),
        'remark': CharField(desc = "备注"),
        'end_time': DateField(desc = "截至时间"),
        'create_time': DateField(desc = "进入时间"),
    }))
    response.total = ResponseField(IntField, desc = "数据总数")
    response.total_page = ResponseField(IntField, desc = "总页码数")

    @classmethod
    def get_desc(cls):
        return "客户销售机会列表接口"

    @classmethod
    def get_author(cls):
        return "fsy"

    def execute(self, request):
        cur_user = self.auth_user
        user_pro = UserRightServer(cur_user)
        if not user_pro._is_admin:
            request.search_info.update({'staff_id__in': user_pro._staff_id_list})
        page_list = SaleChanceServer.search(request.current_page, **request.search_info)
        return page_list

    def fill(self, response, page_list):
        response.data_list = [{
                'id': sale_chance.id,
                'staff_id': sale_chance.staff.id if sale_chance.id else 0,
                'staff_name': sale_chance.staff.name if sale_chance.staff else "",
                'customer_id': sale_chance.customer.id,
                'name': sale_chance.customer.name,
                'gender': sale_chance.customer.gender,
                'birthday': sale_chance.customer.birthday,
                'email': sale_chance.customer.email,
                'phone': sale_chance.customer.phone,
                'wechat': sale_chance.customer.wechat,
                'city': sale_chance.customer.city,
                'address':sale_chance.customer.address,
                'good_name':sale_chance.goods.name if sale_chance.goods else "",
                'good_id':sale_chance.goods.id if sale_chance.goods else 0,
                'remark': sale_chance.remark,
                'end_time': sale_chance.end_time,
                'create_time': sale_chance.create_time,
        } for sale_chance in page_list.data]
        response.total = page_list.total
        response.total_page = page_list.total_page

        return response


class Update(StaffAuthorizedApi):
    """编辑销售机会"""
    request = with_metaclass(RequestFieldSet)
    request.sale_chance_id = RequestField(IntField, desc = "销售机会id")
    request.sale_chance_info = RequestField(DictField, desc = "员工绩效详情", conf = {
        'end_time': DateField(desc = "截至时间", is_required = False),
    })

    response = with_metaclass(ResponseFieldSet)

    @classmethod
    def get_desc(cls):
        return "编辑销售机会接口"

    @classmethod
    def get_author(cls):
        return "fsy"

    def execute(self, request):
        page_list = SaleChanceServer.update(request.sale_chance_id, **request.sale_chance_info)


    def fill(self, response, page_list):

        return response
