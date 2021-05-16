# -*- coding: UTF-8 -*-    
# Author: Dongjd
# FileName: __init__.py
# DateTime: 2020/12/15 15:18
# Project: awesome_dong
# Do Not Touch Me!

from tuoen.abs.agent_service.collection.manager import CollectionServer
from tuoen.agile.agent_apis.base import AgentAccountAuthorizedApi
from tuoen.agile.base import NoAuthrizedApi
from tuoen.sys.core.api.request import RequestField, RequestFieldSet
from tuoen.sys.core.api.response import ResponseField, ResponseFieldSet
from tuoen.sys.core.api.utils import with_metaclass
from tuoen.sys.core.field.base import CharField, DictField, ListField, IntField, DatetimeField, NewDictField


class List(AgentAccountAuthorizedApi):
    """反馈信息列表"""

    request = with_metaclass(RequestFieldSet)
    request.current_page = RequestField(IntField, desc="页码")
    request.query_info = RequestField(DictField, desc='查询条件', conf={
        'form_id': IntField(desc='表单ID', is_required=False),
        'landing_page_id': IntField(desc='投放页ID', is_required=False),
    })

    response = with_metaclass(ResponseFieldSet)

    response.collection_list = ResponseField(ListField, desc="反馈信息列表", fmt=DictField(
        desc="反馈信息", conf={
            'id': IntField(desc="id"),
            'name': CharField(desc="提交人姓名"),
            'address': CharField(desc="提交地点"),
            'detail_data': NewDictField(desc='信息详情'),
            'create_time': DatetimeField(desc='创建时间')

        }
    ))

    response.valid_num = ResponseField(IntField, desc='有效反馈数')

    response.total = ResponseField(IntField, desc="总数")
    response.total_page = ResponseField(IntField, desc="总页数")

    @classmethod
    def get_desc(cls):
        return "反馈信息列表接口"

    @classmethod
    def get_author(cls):
        return "djd"

    @classmethod
    def get_protocol_num(cls):
        return 400001

    def execute(self, request):
        collections, valid_num = CollectionServer.get_n_page(request.current_page, **request.query_info)
        return collections, valid_num

    def fill(self, response, collections, valid_num):
        response.collection_list = [
            {
                'id': customer.id,
                'name': customer.name,
                'address': customer.address,
                'detail_data': customer.detail_data,
                'create_time': customer.create_time
            }
            for customer in collections.data
        ]

        response.valid_num = valid_num
        response.total = collections.total
        response.total_page = collections.total_page
        return response


class Export(AgentAccountAuthorizedApi):
    """
    export feedback information
    """

    request = with_metaclass(RequestFieldSet)
    request.query_info = RequestField(DictField, desc='查询信息', conf={
        'form_id': IntField(desc='表单ID', is_required=False),
        'landing_page_id': IntField(desc='投放页ID', is_required=False),
        'start_time': DatetimeField(desc='开始时间', is_required=False),
        'end_time': DatetimeField(desc='结束时间', is_required=False),
        'template_num': IntField(desc='模板id', is_required=False),
        'export_type': IntField(desc='导出模式: 1： 仅反馈；2：仅附件；3：反馈及附件', is_required=False),
        'sub_export_type': IntField(desc='附件导出子模式：1：按题目分文件夹；2：按反馈分文件夹', is_required=False)
    })

    response = with_metaclass(ResponseFieldSet)

    response.export_file_url = ResponseField(CharField, desc="反馈信息文件地址")

    @classmethod
    def get_desc(cls):
        return "反馈信息导出接口"

    @classmethod
    def get_author(cls):
        return "djd"

    @classmethod
    def get_protocol_num(cls):
        return 400002

    def execute(self, request):
        request.query_info.update({
            'company': self.auth_account.company
        })
        collections_url = CollectionServer.export_by_time_scope(**request.query_info)
        return collections_url

    def fill(self, response, collections_url):
        response.export_file_url = collections_url
        return response


class CollectInfo(NoAuthrizedApi):
    """反馈信息存储"""

    request = with_metaclass(RequestFieldSet)
    request.collect_info = RequestField(DictField, desc='查询信息', conf={
        'form_id': IntField(desc='表单ID', is_required=False),
        'landing_page_id': IntField(desc='投放页ID', is_required=False),
        'detail_data': NewDictField(desc='信息详情'),
    })

    response = with_metaclass(ResponseFieldSet)

    @classmethod
    def get_desc(cls):
        return "反馈信息存储接口（无认证）"

    @classmethod
    def get_author(cls):
        return "djd"

    @classmethod
    def get_protocol_num(cls):
        return 400003

    def execute(self, request):
        if 'landing_page_id' in request.collect_info:
            CollectionServer.process_data('p', **request.collect_info)
        else:
            CollectionServer.process_data('f', **request.collect_info)

    def fill(self, response):
        return response


class TemplateList(AgentAccountAuthorizedApi):
    """反馈信息模板"""

    request = with_metaclass(RequestFieldSet)

    response = with_metaclass(ResponseFieldSet)
    response.template_infos = ResponseField(ListField, desc='模板列表', fmt=DictField(
        desc='模板信息', conf={
            'unique_num': IntField(desc='模板唯一标识'),
            'name': CharField(desc='模板名称')
        }
    ))

    @classmethod
    def get_desc(cls):
        return "反馈信息模板"

    @classmethod
    def get_author(cls):
        return "djd"

    @classmethod
    def get_protocol_num(cls):
        return 400004

    def execute(self, request):
        from tuoen.abs.agent_service.collection.templates import template_tuple_list
        return template_tuple_list

    def fill(self, response, templates):
        response.template_infos = [
            {
                'unique_num': template.unique_num,
                'name': template.name
            }
            for template in templates
        ]
        return response
