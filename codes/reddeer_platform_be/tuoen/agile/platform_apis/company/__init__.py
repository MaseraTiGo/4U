# -*- coding: UTF-8 -*-    
# Author: Dongjd
# FileName: __init__.py
# DateTime: 2020/12/17 18:01
# Project: awesome_dong
# Do Not Touch Me!

from tuoen.abs.platform_service.company.manager import CompanyServer
from tuoen.agile.platform_apis.base import PlatformAccountAuthorizedApi
from tuoen.sys.core.api.request import RequestField, RequestFieldSet
from tuoen.sys.core.api.response import ResponseFieldSet
from tuoen.sys.core.api.utils import with_metaclass
from tuoen.sys.core.field.base import CharField, DictField


class Create(PlatformAccountAuthorizedApi):
    """创建公司"""

    request = with_metaclass(RequestFieldSet)
    request.create_info = RequestField(DictField, desc="新建", conf={
        'name': CharField(desc="公司名"),
        'unique_id': CharField(desc="唯一标识符", is_required=False),
        'address': CharField(desc="地址"),
        'phone': CharField(desc="联系电话"),
        'login_url': CharField(desc="公司网址"),
    })

    response = with_metaclass(ResponseFieldSet)

    @classmethod
    def get_desc(cls):
        return "公司创建接口"

    @classmethod
    def get_author(cls):
        return "djd"

    @classmethod
    def get_protocol_num(cls):
        return 3001

    def execute(self, request):
        CompanyServer.create(**request.create_info)

    def fill(self, response):
        return response
