# -*- coding: UTF-8 -*-    
# Author: Dongjd
# FileName: __init__.py
# DateTime: 2020/12/16 12:07
# Project: awesome_dong
# Do Not Touch Me!

from tuoen.abs.agent_service.event.manager import FormEventServer
from tuoen.abs.agent_service.form.manager import FormServer
from tuoen.agile.agent_apis.base import AgentAccountAuthorizedApi
from tuoen.agile.base import NoAuthrizedApi
from tuoen.sys.core.api.request import RequestField, RequestFieldSet
from tuoen.sys.core.api.response import ResponseField, ResponseFieldSet
from tuoen.sys.core.api.utils import with_metaclass
from tuoen.sys.core.field.base import CharField, DictField, ListField, IntField, BooleanField, DatetimeField, \
    NewDictField


class Create(AgentAccountAuthorizedApi):
    """表单创建"""

    request = with_metaclass(RequestFieldSet)
    request.create_info = RequestField(DictField, desc='表单创建信息', conf={
        'name': CharField(desc='表单名称'),
        'is_title_hide': BooleanField(desc='是否隐藏表头'),
        'is_limited': BooleanField(desc='限填一次'),
        'components': ListField(desc='组件信息', fmt=DictField(desc='组件详情', conf={
            'name': CharField(desc='组件名称（非类型）'),
            'describe': CharField(desc='描述', is_required=False),
            'index': IntField(desc='序位'),
            'is_needed': BooleanField(desc='是否必填'),
            'tag': IntField(desc='组件标识：'
                                 'NAME = 0 PHONE = 1 AGE = 2 GENDER = 3 TEXT = 4 RADIO = 5 '
                                 'ADDRESS = 6 CHECKBOX = 7 PICS = 13 DIY = 14 DOCS =15 ATTACH = 16'
                                 '[(NAME, 姓名), (PHONE, 手机), (AGE, 年龄), (GENDER, 性别), '
                                 '(TEXT, 文本), (RADIO, 单选), (ADDRESS, 地址), (CHECKBOX, 多选), (ATTACH, 附件)],'
                                 '(PICS, 图片), (DIY, 自定义), (DOCS, 文字描述)'),
            'c_type': IntField(
                desc='组件类型:[(TEXT, 文本, 1), (RADIO, 单选, 2), (ADDRESS, 地址, 3), (CHECKBOX, 多选, 4), (PICS, 图片, 5)'
                     '(DIY, 自定义, 6), (DOCS, 文字描述, 7), (ATTACH, 附件, 8)]'),
            'attrs': NewDictField(desc='json dict类型'),
        }))
    })

    response = with_metaclass(ResponseFieldSet)
    response.form_id = ResponseField(IntField, desc='表单id')

    @classmethod
    def get_desc(cls):
        return "表单创建接口"

    @classmethod
    def get_author(cls):
        return "djd"

    @classmethod
    def get_protocol_num(cls):
        return 500001

    def execute(self, request):
        account = self.auth_account
        request.create_info.update({
            'company': account.company,
        })
        form = FormServer.create(**request.create_info)
        FormEventServer.create(**{
            'account': account,
            'action': 0,
            'form': form
        })
        return form.id

    def fill(self, response, form_id):
        response.form_id = form_id
        return response


class Delete(AgentAccountAuthorizedApi):
    """表单删除"""

    request = with_metaclass(RequestFieldSet)
    request.form_id = RequestField(CharField, desc="表单id")

    response = with_metaclass(ResponseFieldSet)

    @classmethod
    def get_desc(cls):
        return "表单删除接口"

    @classmethod
    def get_author(cls):
        return "djd"

    @classmethod
    def get_protocol_num(cls):
        return 500002

    def execute(self, request):
        account = self.auth_account
        form = FormServer.soft_delete(request.form_id)
        FormEventServer.create(**{
            'account': account,
            'action': 1,
            'form': form
        })

    def fill(self, response):
        return response


class List(AgentAccountAuthorizedApi):
    """表单列表"""

    request = with_metaclass(RequestFieldSet)

    response = with_metaclass(ResponseFieldSet)
    response.form_infos = ResponseField(ListField, desc='表单列表', fmt=DictField(desc='表单详情', conf={
        'name': CharField(desc='表单名称'),
        'id': IntField(desc='表单id'),
        'unique_id': CharField(desc='表单唯一标识符'),
    }))

    @classmethod
    def get_desc(cls):
        return "表单列表接口"

    @classmethod
    def get_author(cls):
        return "djd"

    @classmethod
    def get_protocol_num(cls):
        return 500003

    def execute(self, request):
        default_query_info = {'company': self.auth_account.company}
        forms = FormServer.list(**default_query_info)
        return forms

    def fill(self, response, forms):
        response.form_infos = [
            {
                'id': form.id,
                'name': form.name,
                'unique_id': form.unique_id,
            }
            for form in forms
        ]
        return response


class Search(AgentAccountAuthorizedApi):
    """表单列表"""

    request = with_metaclass(RequestFieldSet)
    request.current_page = RequestField(IntField, desc='当前页')
    request.query_info = RequestField(DictField, desc='关键词', conf={
        'keywords': CharField(desc='搜索关键字', is_required=False)
    })

    response = with_metaclass(ResponseFieldSet)
    response.form_infos = ResponseField(ListField, desc='表单列表', fmt=DictField(desc='表单详情', conf={
        'id': IntField(desc='表单id'),
        'name': CharField(desc='表单名称'),
        'status': BooleanField(desc='表单状态'),
        'belong_page': IntField(desc='表单归属页数'),
        'feedback_num': IntField(desc="反馈数"),
        'latest_feedback': DatetimeField(desc="最新反馈时间"),
        'user_name': CharField(desc='创建者姓名'),
        'create_time': DatetimeField(desc='创建时间'),
        'url': CharField(desc='链接'),
        # 'landing_page_ids': ListField(desc='投放页id数组', fmt=IntField(desc='投放页id'))

    }))

    response.total = ResponseField(IntField, desc='总数')
    response.total_page = ResponseField(IntField, desc='总页数')

    @classmethod
    def get_desc(cls):
        return "表单列表接口"

    @classmethod
    def get_author(cls):
        return "djd"

    @classmethod
    def get_protocol_num(cls):
        return 500004

    def execute(self, request):
        account = self.auth_account
        request.query_info.update({
            'company': self.auth_account.company
        })
        forms = FormServer.get_n_page(request.current_page, **request.query_info)
        return forms, account

    def fill(self, response, forms, account):
        response.form_infos = [
            {
                'id': form.id,
                'name': form.name,
                'status': form.is_delete,
                'belong_page': form.landing_pages_num,
                'feedback_num': form.feedback_num,
                'url': form.url,
                'latest_feedback': form.latest_feedback,
                'user_name': form.account.username if hasattr(form, 'account') and form.account else '',
                'create_time': form.create_time,
                # 'landing_page_ids': form.landing_pages_ids,
            }
            for form in forms.data
        ]
        response.total = forms.total
        response.total_page = forms.total_page
        return response


class Copy(AgentAccountAuthorizedApi):
    """创建副本"""

    request = with_metaclass(RequestFieldSet)
    request.form_id = RequestField(IntField, desc="form id")
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
        return 500005

    def execute(self, request):
        form = FormServer.make_fucking_copy_by_id(request.form_id, request.copy_name)
        FormEventServer.create(**{
            'account': self.auth_account,
            'action': 5,
            'form': form,
        })

    def fill(self, response):
        return response


class Rename(AgentAccountAuthorizedApi):
    """重命名"""

    request = with_metaclass(RequestFieldSet)
    request.form_id = RequestField(IntField, desc="form id")
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
        return 500006

    def execute(self, request):
        form = FormServer.rename(request.form_id, request.new_name)
        FormEventServer.create(**{
            'account': self.auth_account,
            'action': 4,
            'form': form,
        })

    def fill(self, response):
        return response


class Get(AgentAccountAuthorizedApi):
    """获取表单"""

    request = with_metaclass(RequestFieldSet)
    request.form_id = RequestField(IntField, desc="form id")

    response = with_metaclass(ResponseFieldSet)
    response.form_info = ResponseField(DictField, desc='表单信息', conf={
        'id': IntField(desc='表单id'),
        'name': CharField(desc='表单名称'),
        'is_limited': BooleanField(desc='限填'),
        'is_title_hide': BooleanField(desc='是否隐藏表头'),
        'url': CharField(desc='表单url'),
        'components': ListField(desc='组件', fmt=DictField(desc='组件详情', conf={
            'id': IntField(desc='组件id'),
            'name': CharField(desc='组件名称'),
            'describe': CharField(desc='组件描述'),
            'is_needed': BooleanField(desc='是否必填'),
            'index': IntField(desc='序位'),
            'tag': IntField(desc='组件标识：'
                                 'NAME = 0 PHONE = 1 AGE = 2 GENDER = 3 TEXT = 4 RADIO = 5 '
                                 'ADDRESS = 6 CHECKBOX = 7 ATTACH = 16'
                                 '[(NAME, 姓名), (PHONE, 手机), (AGE, 年龄), (GENDER, 性别), '
                                 '(TEXT, 文本), (RADIO, 单选), (ADDRESS, 地址), (CHECKBOX, 多选), (ATTACH, 附件)]'),
            'c_type': IntField(desc='组件类型: [(TEXT, 文本, 1), (RADIO, 单选, 2),'
                                    ' (ADDRESS, 地址, 3), (CHECKBOX, 多选, 4), (ATTACH, 附件, 8)]'),
            'attrs': NewDictField(desc='扩展属性'),
        }))

    })

    @classmethod
    def get_desc(cls):
        return "获取表单接口"

    @classmethod
    def get_author(cls):
        return "djd"

    @classmethod
    def get_protocol_num(cls):
        return 500007

    def execute(self, request):
        form, components = FormServer.get_form_and_components(request.form_id)
        return form, components

    def fill(self, response, form, components):
        response.form_info = {
            'id': form.id,
            'name': form.name,
            'is_limited': form.is_limited,
            'is_title_hide': form.is_title_hide,
            'url': form.url,
            'components': [{
                'id': component.id,
                'name': component.name,
                'describe': component.describe,
                'is_needed': component.is_needed,
                'index': component.index,
                'tag': component.tag,
                'c_type': component.c_type,
                'attrs': component.attrs
            }
                for component in components
            ]

        }
        return response


class MultiGet(AgentAccountAuthorizedApi):
    """获取多个表单"""

    request = with_metaclass(RequestFieldSet)
    request.form_ids = RequestField(ListField, desc='id数组', fmt=IntField(desc="form id"))

    response = with_metaclass(ResponseFieldSet)
    response.form_infos = ResponseField(ListField, desc='表单信息列表', fmt=DictField(desc='表单信息', conf={
        'id': IntField(desc='表单id'),
        'name': CharField(desc='表单名称'),
        'is_limited': BooleanField(desc='限填'),
        'is_title_hide': BooleanField(desc='是否隐藏表头'),
        'url': CharField(desc='表单url'),
        'components': ListField(desc='组件', fmt=DictField(desc='组件详情', conf={
            'id': IntField(desc='组件id'),
            'name': CharField(desc='组件名称'),
            'is_needed': BooleanField(desc='是否必填'),
            'index': IntField(desc='序位'),
            'tag': IntField(desc='组件标识：'
                                 'NAME = 0 PHONE = 1 AGE = 2 GENDER = 3 TEXT = 4 RADIO = 5 '
                                 'ADDRESS = 6 CHECKBOX = 7 ATTACH = 16'
                                 '[(NAME, 姓名), (PHONE, 手机), (AGE, 年龄), (GENDER, 性别), '
                                 '(TEXT, 文本), (RADIO, 单选), (ADDRESS, 地址), (CHECKBOX, 多选), , (ATTACH, 附件)]'),
            'c_type': IntField(desc='组件类型: [(TEXT, 文本, 1), (RADIO, 单选, 2),'
                                    ' (ADDRESS, 地址, 3), (CHECKBOX, 多选, 4), (ATTACH, 附件, 8)]'),
            'attrs': NewDictField(desc='扩展属性')
        }))

    }))

    @classmethod
    def get_desc(cls):
        return "获取多个表单接口"

    @classmethod
    def get_author(cls):
        return "djd"

    @classmethod
    def get_protocol_num(cls):
        return 500008

    def execute(self, request):
        form_infos = FormServer.multi_get_form_and_components(request.form_ids)
        return form_infos

    def fill(self, response, form_infos):
        response.form_infos = [
            {
                'id': form.id,
                'name': form.name,
                'is_limited': form.is_limited,
                'is_title_hide': form.is_title_hide,
                'url': form.url,
                'components': [
                    {
                        'id': component.id,
                        'name': component.name,
                        'is_needed': component.is_needed,
                        'index': component.index,
                        'tag': component.tag,
                        'c_type': component.c_type,
                        'attrs': component.attrs
                    }
                    for component in components
                ]

            }
            for form, components in form_infos
        ]
        return response


class Publish(AgentAccountAuthorizedApi):
    """发布表单"""

    request = with_metaclass(RequestFieldSet)
    request.form_id = RequestField(IntField, desc='表单的id')

    response = with_metaclass(ResponseFieldSet)
    response.url = ResponseField(CharField, desc='投放表单URL')

    @classmethod
    def get_desc(cls):
        return "表单发布接口"

    @classmethod
    def get_author(cls):
        return "djd"

    @classmethod
    def get_protocol_num(cls):
        return 500009

    def execute(self, request):
        url = FormServer.publish(request.form_id)
        return url

    def fill(self, response, url):
        response.url = url
        return response


class PublicGet(NoAuthrizedApi):
    """获取表单"""

    request = with_metaclass(RequestFieldSet)
    request.form_id = RequestField(IntField, desc="form id")

    response = with_metaclass(ResponseFieldSet)
    response.form_info = ResponseField(DictField, desc='表单信息', conf={
        'id': IntField(desc='表单id'),
        'name': CharField(desc='表单名称'),
        'is_limited': BooleanField(desc='限填'),
        'is_title_hide': BooleanField(desc='是否隐藏表头'),
        'url': CharField(desc='表单url'),
        'components': ListField(desc='组件', fmt=DictField(desc='组件详情', conf={
            'id': IntField(desc='组件id'),
            'name': CharField(desc='组件名称'),
            'describe': CharField(desc='组件描述'),
            'is_needed': BooleanField(desc='是否必填'),
            'index': IntField(desc='序位'),
            'tag': IntField(desc='组件标识：'
                                 'NAME = 0 PHONE = 1 AGE = 2 GENDER = 3 TEXT = 4 RADIO = 5 '
                                 'ADDRESS = 6 CHECKBOX = 7 ATTACH = 16'
                                 '[(NAME, 姓名), (PHONE, 手机), (AGE, 年龄), (GENDER, 性别), '
                                 '(TEXT, 文本), (RADIO, 单选), (ADDRESS, 地址), (CHECKBOX, 多选), (ATTACH, 附件)]'),
            'c_type': IntField(desc='组件类型: [(TEXT, 文本, 1), (RADIO, 单选, 2),'
                                    ' (ADDRESS, 地址, 3), (CHECKBOX, 多选, 4), (ATTACH, 附件, 8)]'),
            'attrs': NewDictField(desc='扩展属性'),
        }))

    })

    @classmethod
    def get_desc(cls):
        return "获取表单接口(无认证)"

    @classmethod
    def get_author(cls):
        return "djd"

    @classmethod
    def get_protocol_num(cls):
        return 500010

    def execute(self, request):
        form, components = FormServer.get_form_and_components(request.form_id)
        return form, components

    def fill(self, response, form, components):
        response.form_info = {
            'id': form.id,
            'name': form.name,
            'is_limited': form.is_limited,
            'is_title_hide': form.is_title_hide,
            'url': form.url,
            'components': [{
                'id': component.id,
                'name': component.name,
                'describe': component.describe,
                'is_needed': component.is_needed,
                'index': component.index,
                'tag': component.tag,
                'c_type': component.c_type,
                'attrs': component.attrs
            }
                for component in components
            ]

        }
        return response


class PublicMultiGet(NoAuthrizedApi):
    """获取多个表单"""

    request = with_metaclass(RequestFieldSet)
    request.form_ids = RequestField(ListField, desc='id数组', fmt=IntField(desc="form id"))

    response = with_metaclass(ResponseFieldSet)
    response.form_infos = ResponseField(ListField, desc='表单信息列表', fmt=DictField(desc='表单信息', conf={
        'id': IntField(desc='表单id'),
        'name': CharField(desc='表单名称'),
        'is_limited': BooleanField(desc='限填'),
        'is_title_hide': BooleanField(desc='是否隐藏表头'),
        'url': CharField(desc='表单url'),
        'components': ListField(desc='组件', fmt=DictField(desc='组件详情', conf={
            'id': IntField(desc='组件id'),
            'name': CharField(desc='组件名称'),
            'is_needed': BooleanField(desc='是否必填'),
            'index': IntField(desc='序位'),
            'tag': IntField(desc='组件标识：'
                                 'NAME = 0 PHONE = 1 AGE = 2 GENDER = 3 TEXT = 4 RADIO = 5 '
                                 'ADDRESS = 6 CHECKBOX = 7 ATTACH = 16'
                                 '[(NAME, 姓名), (PHONE, 手机), (AGE, 年龄), (GENDER, 性别), '
                                 '(TEXT, 文本), (RADIO, 单选), (ADDRESS, 地址), (CHECKBOX, 多选), (ATTACH, 附件)]'),
            'c_type': IntField(desc='组件类型: [(TEXT, 文本, 1), (RADIO, 单选, 2),'
                                    ' (ADDRESS, 地址, 3), (CHECKBOX, 多选, 4), (ATTACH, 附件, 8)]'),
            'attrs': NewDictField(desc='扩展属性')
        }))

    }))

    @classmethod
    def get_desc(cls):
        return "获取多个表单接口(无认证)"

    @classmethod
    def get_author(cls):
        return "djd"

    @classmethod
    def get_protocol_num(cls):
        return 500011

    def execute(self, request):
        form_infos = FormServer.multi_get_form_and_components(request.form_ids)
        return form_infos

    def fill(self, response, form_infos):
        response.form_infos = [
            {
                'id': form.id,
                'name': form.name,
                'is_limited': form.is_limited,
                'is_title_hide': form.is_title_hide,
                'url': form.url,
                'components': [
                    {
                        'id': component.id,
                        'name': component.name,
                        'is_needed': component.is_needed,
                        'index': component.index,
                        'tag': component.tag,
                        'c_type': component.c_type,
                        'attrs': component.attrs
                    }
                    for component in components
                ]

            }
            for form, components in form_infos
        ]
        return response


class RelativeLandingPage(AgentAccountAuthorizedApi):
    """附属投放页"""

    request = with_metaclass(RequestFieldSet)
    request.form_id = RequestField(IntField, desc="表单id")

    response = with_metaclass(ResponseFieldSet)
    response.landing_pages = ResponseField(ListField, desc='附属投放页数组', fmt=DictField(desc='附属投放页', conf={
        'id': IntField(desc='投放页id'),
        'name': CharField(desc='投放页名字')
    }))

    @classmethod
    def get_desc(cls):
        return "表单附属投放页接口"

    @classmethod
    def get_author(cls):
        return "djd"

    @classmethod
    def get_protocol_num(cls):
        return 500012

    def execute(self, request):
        landing_page_qs = FormServer.get_relative_landing_page(request.form_id)
        return landing_page_qs

    def fill(self, response, landing_page_qs):
        response.landing_pages = [
            {
                'id': landing_page.id,
                'name': landing_page.name
            }
            for landing_page in landing_page_qs
        ]
        return response


class Edit(AgentAccountAuthorizedApi):
    """表单编辑"""

    request = with_metaclass(RequestFieldSet)
    request.edit_info = RequestField(DictField, desc='表单编辑信息', conf={
        'id': IntField(desc='表单id'),
        'name': CharField(desc='表单名称'),
        'is_title_hide': BooleanField(desc='是否隐藏表头'),
        'is_limited': BooleanField(desc='限填一次'),
        'components': ListField(desc='组件信息', fmt=DictField(desc='组件详情', conf={
            'name': CharField(desc='组件名称（非类型）'),
            'describe': CharField(desc='描述', is_required=False),
            'index': IntField(desc='序位'),
            'is_needed': BooleanField(desc='是否必填'),
            'tag': IntField(desc='组件标识：'
                                 'NAME = 0 PHONE = 1 AGE = 2 GENDER = 3 TEXT = 4 RADIO = 5 '
                                 'ADDRESS = 6 CHECKBOX = 7 PICS = 13 DIY = 14 DOCS =15, ATTACH = 16'
                                 '[(NAME, 姓名), (PHONE, 手机), (AGE, 年龄), (GENDER, 性别), '
                                 '(TEXT, 文本), (RADIO, 单选), (ADDRESS, 地址), (CHECKBOX, 多选), (ATTACH, 附件)], '
                                 '(PICS, 图片), (DIY, 自定义), (DOCS, 文字描述)'),
            'c_type': IntField(desc='组件类型:[(TEXT, 文本, 1), (RADIO, 单选, 2), (ADDRESS, 地址, 3), (CHECKBOX, 多选, 4),'
                                    '(PICS, 图片, 5), (DIY, 自定义, 6), (DOCS, 文字描述, 7), (ATTACH, 附件, 8)]'),
            'attrs': NewDictField(desc='json dict类型'),
        }))
    })

    response = with_metaclass(ResponseFieldSet)
    response.form_id = ResponseField(IntField, desc='表单id')

    @classmethod
    def get_desc(cls):
        return "表单编辑接口"

    @classmethod
    def get_author(cls):
        return "djd"

    @classmethod
    def get_protocol_num(cls):
        return 500013

    def execute(self, request):
        account = self.auth_account
        request.edit_info.update({
            'company': account.company,
        })
        form = FormServer.edit(**request.edit_info)
        FormEventServer.create(**{
            'account': account,
            'action': 2,
            'form': form
        })
        return form.id

    def fill(self, response, form_id):
        response.form_id = form_id
        return response


class Fuzzy(AgentAccountAuthorizedApi):
    """表单模糊搜索"""

    request = with_metaclass(RequestFieldSet)
    request.search_info = RequestField(DictField, desc='搜索信息', conf={
        'keywords': CharField(desc='关键字', is_required=False)
    })

    response = with_metaclass(ResponseFieldSet)
    response.form_infos = ResponseField(ListField, desc='表单列表', fmt=DictField(desc='表单详情', conf={
        'name': CharField(desc='表单名称'),
        'id': IntField(desc='表单id'),
    }))

    @classmethod
    def get_desc(cls):
        return "表单模糊搜索接口"

    @classmethod
    def get_author(cls):
        return "djd"

    @classmethod
    def get_protocol_num(cls):
        return 500014

    def execute(self, request):
        default_query_info = {'company': self.auth_account.company}
        if 'keywords' in request.search_info:
            default_query_info.update({
                'name__icontains': request.search_info.pop('keywords')
            })
        forms = FormServer.list(**default_query_info)
        return forms

    def fill(self, response, forms):
        response.form_infos = [
            {
                'id': form.id,
                'name': form.name,
            }
            for form in forms
        ]
        return response
