# -*- coding: UTF-8 -*-    
# Author: Dongjd
# FileName: __init__.py
# DateTime: 2020/12/14 15:56
# Project: operate_backend_be
# Do Not Touch Me!

from tuoen.abs.agent_service.event.manager import LandingPageEventServer
from tuoen.abs.agent_service.landingpage.manager import LandingPageServer
from tuoen.agile.agent_apis.base import AgentAccountAuthorizedApi
from tuoen.agile.base import NoAuthrizedApi
from tuoen.sys.core.api.request import RequestField, RequestFieldSet
from tuoen.sys.core.api.response import ResponseField, ResponseFieldSet
from tuoen.sys.core.api.utils import with_metaclass
from tuoen.sys.core.field.base import CharField, DictField, ListField, IntField, DatetimeField, NewDictField


class List(AgentAccountAuthorizedApi):
    """投放页列表"""

    request = with_metaclass(RequestFieldSet)
    request.current_page = RequestField(IntField, desc="页码")
    request.search_info = RequestField(DictField, desc="搜索条件", conf={
        'keywords': CharField(desc='关键词', is_required=False)
    })

    response = with_metaclass(ResponseFieldSet)

    response.landing_page_list = ResponseField(ListField, desc="投放页列表", fmt=DictField(
        desc="投放页信息", conf={
            'id': IntField(desc="id"),
            'name': CharField(desc="投放页名称"),
            'status': IntField(desc="状态：UNPUBLISHED = 0 PUBLISHED = 1 SUSPEND = 2 DELETE = 3 "
                                    "[(UNPUBLISHED, 未发布), (PUBLISHED, 投放中), (SUSPEND, 停止), (DELETE, 删除)]"),
            'feedback_num': IntField(desc="反馈数"),
            'latest_feedback': DatetimeField(desc="最新反馈时间"),
            'user_name': CharField(desc='创建者姓名'),
            'url': CharField(desc='链接'),
            # 'form_ids': ListField(desc='链接', fmt=IntField(desc='表单id数组')),
            'create_time': DatetimeField(desc='创建时间')

        }
    ))

    response.total = ResponseField(IntField, desc="总数")
    response.total_page = ResponseField(IntField, desc="总页数")

    @classmethod
    def get_desc(cls):
        return "投放页列表接口"

    @classmethod
    def get_author(cls):
        return "djd"

    @classmethod
    def get_protocol_num(cls):
        return 300001

    def execute(self, request):
        default_query_info = {'company': self.auth_account.company}
        default_query_info.update(request.search_info)
        landing_pages = LandingPageServer.landing_pages(request.current_page, **default_query_info)
        LandingPageServer.get_feedback_num_and_latest_time(landing_pages.data)
        return landing_pages

    def fill(self, response, landing_pages):
        response.landing_page_list = [
            {
                'id': landing_page.id,
                'name': landing_page.name,
                'status': landing_page.status,
                'feedback_num': landing_page.feedback_num,
                'url': landing_page.url,
                # 'form_ids': landing_page.form_ids,
                'latest_feedback': landing_page.latest_feedback,
                'user_name': landing_page.account.username if landing_page.account else '',
                'create_time': landing_page.create_time
            }
            for landing_page in landing_pages.data
        ]
        response.total = landing_pages.total
        response.total_page = landing_pages.total_page
        return response


class Copy(AgentAccountAuthorizedApi):
    """创建副本"""

    request = with_metaclass(RequestFieldSet)
    request.landing_page_id = RequestField(IntField, desc="投放页id")
    request.copy_name = RequestField(CharField, desc='副本名称')

    response = with_metaclass(ResponseFieldSet)

    @classmethod
    def get_desc(cls):
        return "创建投放页副本接口"

    @classmethod
    def get_author(cls):
        return "djd"

    @classmethod
    def get_protocol_num(cls):
        return 300002

    def execute(self, request):
        landing_page = LandingPageServer.make_fucking_copy_by_id(request.landing_page_id, request.copy_name,
                                                                 self.auth_account)
        LandingPageEventServer.create(**{
            'account': self.auth_account,
            'action': 5,
            'landing_page': landing_page,
        })

    def fill(self, response):
        return response


class Rename(AgentAccountAuthorizedApi):
    """重命名"""

    request = with_metaclass(RequestFieldSet)
    request.landing_page_id = RequestField(IntField, desc="投放页id")
    request.new_name = RequestField(CharField, desc="新名字")

    response = with_metaclass(ResponseFieldSet)

    @classmethod
    def get_desc(cls):
        return "重命名接口"

    @classmethod
    def get_author(cls):
        return "djd"

    @classmethod
    def get_protocol_num(cls):
        return 300003

    def execute(self, request):
        landing_page = LandingPageServer.rename(request.landing_page_id, request.new_name)
        LandingPageEventServer.create(**{
            'account': self.auth_account,
            'action': 4,
            'landing_page': landing_page,
        })

    def fill(self, response):
        return response


class StatusChange(AgentAccountAuthorizedApi):
    """状态更改"""

    request = with_metaclass(RequestFieldSet)
    request.landing_page_id = RequestField(IntField, desc="投放页id")
    request.status = RequestField(IntField, desc="状态值:UNPUBLISHED = 0 PUBLISHED = 1 SUSPEND = 2 DELETE = 3 "
                                                 "[(UNPUBLISHED, 未发布), (PUBLISHED, 投放中), (SUSPEND, 停止), (DELETE, 删除)]")

    response = with_metaclass(ResponseFieldSet)

    @classmethod
    def get_desc(cls):
        return "状态更改接口"

    @classmethod
    def get_author(cls):
        return "djd"

    @classmethod
    def get_protocol_num(cls):
        return 300004

    def execute(self, request):
        LandingPageServer.status_change_to(request.landing_page_id, request.status)

    def fill(self, response):
        return response


class Create(AgentAccountAuthorizedApi):
    """投放页创建"""

    request = with_metaclass(RequestFieldSet)
    request.create_info = RequestField(DictField, desc="创建信息", conf={
        'name': CharField(desc='投放页名称'),
        'url': CharField(desc='投放页url', is_required=False),
        # 'id': IntField(desc='表单id', is_required=False),
        'components': ListField(desc='组件', fmt=DictField(desc='组件详情', conf={
            'index': IntField(desc='序位'),
            # 'is_clicked': BooleanField(desc='是否被点击'),
            'name': CharField(desc='组件名称（非类型）', is_required=False),
            'c_type': IntField(desc="组件类型: PIC = 0 BTN = 1 SLID = 2 FORM = 3 DOCS = 4"
                                    "[(PIC, 图片), (BTN, 按钮), (SLID, 轮播), (FORM, 表单)]"
                                    "(DOCS, 文字描述)"),
            'attrs': NewDictField(desc='json dict类型'),
        }), is_required=False)
    })

    response = with_metaclass(ResponseFieldSet)
    response.landing_page_id = ResponseField(IntField, desc='投放页id')

    @classmethod
    def get_desc(cls):
        return "投放页创建接口"

    @classmethod
    def get_author(cls):
        return "djd"

    @classmethod
    def get_protocol_num(cls):
        return 300005

    def execute(self, request):
        request.create_info.update({
            'company': self.auth_account.company if self.auth_account.company else '',
            'account': self.auth_account
        })
        landing_page = LandingPageServer.create(**request.create_info)
        LandingPageEventServer.create(**{
            'account': self.auth_account,
            'action': 0,
            'landing_page': landing_page,
        })
        return landing_page.id

    def fill(self, response, landing_page_id):
        response.landing_page_id = landing_page_id
        return response


class Get(AgentAccountAuthorizedApi):
    """获取投放页"""

    request = with_metaclass(RequestFieldSet)
    request.landing_page_id = RequestField(IntField, desc="landing page id")

    response = with_metaclass(ResponseFieldSet)
    response.landing_page_info = ResponseField(DictField, desc='投放页信息', conf={
        'id': IntField(desc='投放页id'),
        'name': CharField(desc='投放页名称'),
        'url': CharField(desc='表单url'),
        'components': ListField(desc='组件', fmt=DictField(desc='组件详情', conf={
            'id': IntField(desc='组件id'),
            'name': CharField(desc='组件名称'),
            'index': IntField(desc='序位'),
            'c_type': IntField(desc="组件类型: PIC = 0 BTN = 1 SLID = 2 FORM = 3 "
                                    "[(PIC, 图片), (BTN, 按钮), (SLID, 轮播), (FORM, 表单)]"),
            'attrs': NewDictField(desc='扩展属性')
        }))

    })

    @classmethod
    def get_desc(cls):
        return "获取投放页接口"

    @classmethod
    def get_author(cls):
        return "djd"

    @classmethod
    def get_protocol_num(cls):
        return 300006

    def execute(self, request):
        landing_page, components = LandingPageServer.get_landing_page_and_components(request.landing_page_id)
        return landing_page, components

    def fill(self, response, landing_page, components):
        response.landing_page_info = {
            'id': landing_page.id,
            'name': landing_page.name,
            'url': landing_page.url,
            'components': [{
                'id': component.id,
                'name': component.name,
                'index': component.index,
                'c_type': component.c_type,
                'attrs': component.attrs
            }
                for component in components
            ]

        }
        return response


class Edit(AgentAccountAuthorizedApi):
    """投放页编辑"""

    request = with_metaclass(RequestFieldSet)
    request.landing_page_id = RequestField(IntField, desc='投放页的id')
    request.edit_info = RequestField(DictField, desc="创建信息", conf={
        'name': CharField(desc='投放页名称', is_required=False),
        'url': CharField(desc='投放页url', is_required=False),
        'components': ListField(desc='组件', fmt=DictField(desc='组件详情', conf={
            'id': IntField(desc='组件id:只有id标识去除该组件，没有id表示新增组件，有id和其他内容表示更新', is_required=False),
            'index': IntField(desc='序位', is_required=False),
            'name': CharField(desc='组件名称（非类型）', is_required=False),
            'c_type': IntField(desc="组件类型: PIC = 0 BTN = 1 SLID = 2 FORM = 3 "
                                    "[(PIC, 图片), (BTN, 按钮), (SLID, 轮播), (FORM, 表单)]", is_required=False),
            'attrs': NewDictField(desc='json dict类型', is_required=False),
        }), is_required=False)
    })

    response = with_metaclass(ResponseFieldSet)

    @classmethod
    def get_desc(cls):
        return "投放页编辑接口"

    @classmethod
    def get_author(cls):
        return "djd"

    @classmethod
    def get_protocol_num(cls):
        return 300007

    def execute(self, request):
        account = self.auth_account
        LandingPageServer.edit(account, request.landing_page_id, **request.edit_info)

    def fill(self, response):
        return response


class Publish(AgentAccountAuthorizedApi):
    """发布投放页"""
    request = with_metaclass(RequestFieldSet)
    request.landing_page_id = RequestField(IntField, desc='投放页的id')

    response = with_metaclass(ResponseFieldSet)
    response.url = ResponseField(CharField, desc="投放页URL")

    @classmethod
    def get_desc(cls):
        return "发布投放页接口"

    @classmethod
    def get_author(cls):
        return "djd"

    @classmethod
    def get_protocol_num(cls):
        return 300008

    def execute(self, request):
        url = LandingPageServer.publish(request.landing_page_id)
        return url

    def fill(self, response, url):
        response.url = url
        return response


class ListAll(AgentAccountAuthorizedApi):
    """投放页列表(简要)"""

    request = with_metaclass(RequestFieldSet)

    response = with_metaclass(ResponseFieldSet)

    response.landing_page_list = ResponseField(ListField, desc="投放页列表", fmt=DictField(
        desc="投放页信息", conf={
            'id': IntField(desc="id"),
            'name': CharField(desc="投放页名称"),
        }
    ))

    @classmethod
    def get_desc(cls):
        return "投放页列表(简要)接口"

    @classmethod
    def get_author(cls):
        return "djd"

    @classmethod
    def get_protocol_num(cls):
        return 300009

    def execute(self, request):
        default_query_info = {'company': self.auth_account.company}
        landing_pages = LandingPageServer.brief_info(**default_query_info)
        return landing_pages

    def fill(self, response, landing_pages):
        response.landing_page_list = [
            {
                'id': landing_page.id,
                'name': landing_page.name,
            }
            for landing_page in landing_pages
        ]
        return response


class Delete(AgentAccountAuthorizedApi):
    """投放页删除"""

    request = with_metaclass(RequestFieldSet)
    request.landing_page_id = RequestField(IntField, desc="投放页id")

    response = with_metaclass(ResponseFieldSet)

    @classmethod
    def get_desc(cls):
        return "投放页删除接口"

    @classmethod
    def get_author(cls):
        return "djd"

    @classmethod
    def get_protocol_num(cls):
        return 300010

    def execute(self, request):
        LandingPageServer.delete(request.landing_page_id)

    def fill(self, response):
        return response


class PublicGet(NoAuthrizedApi):
    """获取投放页"""

    request = with_metaclass(RequestFieldSet)
    request.landing_page_id = RequestField(IntField, desc="landing page id")

    response = with_metaclass(ResponseFieldSet)
    response.landing_page_info = ResponseField(DictField, desc='投放页信息', conf={
        'id': IntField(desc='投放页id'),
        'name': CharField(desc='投放页名称'),
        'url': CharField(desc='表单url'),
        'components': ListField(desc='组件', fmt=DictField(desc='组件详情', conf={
            'id': IntField(desc='组件id'),
            'name': CharField(desc='组件名称'),
            'index': IntField(desc='序位'),
            'c_type': IntField(desc="组件类型: PIC = 0 BTN = 1 SLID = 2 FORM = 3 "
                                    "[(PIC, 图片), (BTN, 按钮), (SLID, 轮播), (FORM, 表单)]"),
            'attrs': NewDictField(desc='扩展属性')
        }))

    })

    @classmethod
    def get_desc(cls):
        return "获取投放页接口(无认证)"

    @classmethod
    def get_author(cls):
        return "djd"

    @classmethod
    def get_protocol_num(cls):
        return 300011

    def execute(self, request):
        landing_page, components = LandingPageServer.get_landing_page_and_components(request.landing_page_id,
                                                                                     auth=False)
        return landing_page, components

    def fill(self, response, landing_page, components):
        response.landing_page_info = {
            'id': landing_page.id,
            'name': landing_page.name,
            'url': landing_page.url,
            'components': [{
                'id': component.id,
                'name': component.name,
                'index': component.index,
                'c_type': component.c_type,
                'attrs': component.attrs
            }
                for component in components
            ]

        }
        return response


class RelativeForm(AgentAccountAuthorizedApi):
    """关联表单"""

    request = with_metaclass(RequestFieldSet)
    request.landing_page_id = RequestField(IntField, desc="投放页id")

    response = with_metaclass(ResponseFieldSet)
    response.forms = ResponseField(ListField, desc='关联表单id数组', fmt=DictField(desc='关联表单', conf={
        'id': IntField(desc='表单id'),
        'name': CharField(desc='表单名字'),
    }))

    @classmethod
    def get_desc(cls):
        return "投放页关联表单接口"

    @classmethod
    def get_author(cls):
        return "djd"

    @classmethod
    def get_protocol_num(cls):
        return 300012

    def execute(self, request):
        form_qs = LandingPageServer.get_relative_form(request.landing_page_id)
        return form_qs

    def fill(self, response, form_qs):
        response.forms = [
            {
                'id': form.id,
                'name': form.name
            }
            for form in form_qs
        ]
        return response


class PreView(NoAuthrizedApi):
    """预览投放页"""

    request = with_metaclass(RequestFieldSet)
    request.landing_page_id = RequestField(IntField, desc="landing page id")

    response = with_metaclass(ResponseFieldSet)
    response.landing_page_info = ResponseField(DictField, desc='投放页信息', conf={
        'id': IntField(desc='投放页id'),
        'name': CharField(desc='投放页名称'),
        'url': CharField(desc='表单url'),
        'components': ListField(desc='组件', fmt=DictField(desc='组件详情', conf={
            'id': IntField(desc='组件id'),
            'name': CharField(desc='组件名称'),
            'index': IntField(desc='序位'),
            'c_type': IntField(desc="组件类型: PIC = 0 BTN = 1 SLID = 2 FORM = 3 "
                                    "[(PIC, 图片), (BTN, 按钮), (SLID, 轮播), (FORM, 表单)]"),
            'attrs': NewDictField(desc='扩展属性')
        }))

    })

    @classmethod
    def get_desc(cls):
        return "预览投放页接口(无认证)"

    @classmethod
    def get_author(cls):
        return "djd"

    @classmethod
    def get_protocol_num(cls):
        return 300013

    def execute(self, request):
        landing_page, components = LandingPageServer.preview_landing_page_and_components(request.landing_page_id)
        return landing_page, components

    def fill(self, response, landing_page, components):
        response.landing_page_info = {
            'id': landing_page.id,
            'name': landing_page.name,
            'url': landing_page.url,
            'components': [{
                'id': component.id,
                'name': component.name,
                'index': component.index,
                'c_type': component.c_type,
                'attrs': component.attrs
            }
                for component in components
            ]

        }
        return response
