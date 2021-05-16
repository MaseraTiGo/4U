# -*- coding: UTF-8 -*-    
# Author: Dongjd
# FileName: manager
# DateTime: 2020/12/14 15:58
# Project: operate_backend_be
# Do Not Touch Me!

import datetime

from model.store.model_component import LandingPageComponent
from model.store.model_forms import Form
from model.store.model_landingpage import LandingPage
from model.store.utils import generate_uuid
from tuoen.abs.agent_service.component.manager import LandingPageComponentServer
from tuoen.abs.agent_service.form.manager import FormServer
from tuoen.sys.core.exception.business_error import BusinessError
from tuoen.sys.utils.common.split_page import Splitor

from tuoen.abs.agent_service.customer.manager import CustomerServer


class LandingPageServer(object):
    @classmethod
    def create(cls, **create_info):
        account = create_info.get('account')
        components = None
        if 'components' in create_info:
            components = create_info.pop('components')
        landing_page = LandingPage.create(**create_info)
        if not landing_page:
            raise BusinessError('投放页创建失败')
        for component in components:
            if component.get('c_type') == LandingPageComponent.CType.FORM:
                form_id = FormServer.update_or_create(component, account)
                component.update({'attrs': {'form_id': form_id}})
        if components:
            LandingPageComponentServer.bulk_create(landing_page, components)
        return landing_page

    @classmethod
    def hung_form_ids(cls, landing_page_qs):
        for landing_page in landing_page_qs:
            form_ids = []
            components = landing_page.landing_page_components.all()
            for component in components:
                if component.c_type == LandingPageComponent.CType.FORM:
                    form_ids.append(component.attrs.get('form_id'))
            landing_page.form_ids = form_ids

    @classmethod
    def landing_pages(cls, current_page, **query_info):
        if 'keywords' in query_info:
            keywords = query_info.pop('keywords')
            query_info.update({'name__icontains': keywords})
        landing_page_qs = LandingPage.search(**query_info).exclude(status=LandingPage.Status.DELETE).order_by(
            '-create_time')
        # cls.hung_form_ids(landing_page_qs)
        return Splitor(current_page, landing_page_qs, size=20)

    @classmethod
    def get_feedback_num_and_latest_time(cls, landing_page_qs):
        for landing_page in landing_page_qs:
            collection_qs = landing_page.landing_page_customers.all().order_by('-create_time')
            landing_page.latest_feedback = datetime.datetime.now()
            landing_page.feedback_num = 0

            if collection_qs:
                landing_page.latest_feedback = collection_qs[0].create_time
                landing_page.feedback_num = collection_qs.count()

    @classmethod
    def get_landing_page_by_id(cls, landing_page_id):
        landing_page = LandingPage.search(id=landing_page_id).first()
        if not landing_page:
            raise BusinessError('投放页不存在')
        return landing_page

    @classmethod
    def make_fucking_copy_by_id(cls, landing_page_id, copy_name, account):
        landing_page = cls.get_landing_page_by_id(landing_page_id)
        components = landing_page.landing_page_components.all()
        now = datetime.datetime.now()
        landing_page.pk = None
        landing_page.name = copy_name
        landing_page.unique_id = generate_uuid(LandingPage.PREFIX)
        landing_page.status = LandingPage.Status.UNPUBLISHED
        landing_page.url = ''
        landing_page.create_time = now
        landing_page.account_id = account.id
        landing_page.save()
        # from django.conf import settings
        # actual_url = "{d}/show/showpage?id={u}".format(d=settings.HOST_DOMAIN_PUBLISH, u=landing_page.id)
        # landing_page.update(url=actual_url)
        for component in components:
            component.pk = None
            component.landing_page = landing_page
            component.create_time = now
            component.save()
        return landing_page

    @classmethod
    def rename(cls, landing_page_id, new_name):
        landing_page = cls.get_landing_page_by_id(landing_page_id)
        landing_page.name = new_name
        landing_page.save()
        return landing_page

    @classmethod
    def status_change_to(cls, landing_page_id, status):
        if status not in LandingPage.STATUS_ENUM:
            raise BusinessError('无此状态!')
        landing_page = cls.get_landing_page_by_id(landing_page_id)
        landing_page.status = status
        landing_page.save()

    @classmethod
    def render_form(cls, form, components):
        attrs = {
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
        return attrs

    @classmethod
    def get_landing_page_and_components(cls, landing_page_id, auth=True):
        landing_page = LandingPage.get_byid(landing_page_id)
        if not landing_page:
            raise BusinessError('投放页不存在')
        if auth:
            if landing_page.status == LandingPage.Status.DELETE:
                raise BusinessError('当前投放页状态异常！')
        else:
            if landing_page.status != LandingPage.Status.PUBLISHED:
                raise BusinessError('当前投放页状态异常！')
        components = landing_page.landing_page_components.all()
        for component in components:
            if component.c_type == LandingPageComponent.CType.FORM:
                form_id = component.attrs.get('form_id')
                form, form_components = FormServer.get_form_and_components(form_id)
                form_attrs = cls.render_form(form, form_components)
                component.attrs = form_attrs
        return landing_page, components

    @classmethod
    def edit(cls, account, landing_page_id, **edit_info):
        components = []
        if 'components' in edit_info:
            components = edit_info.pop('components')
        landing_page = cls.get_landing_page_by_id(landing_page_id)
        landing_page.landing_page_components.all().delete()
        landing_page.update(**edit_info)

        for component in components:
            component.update({'landing_page': landing_page})
            if component.get('c_type') == LandingPageComponent.CType.FORM:
                form_id = FormServer.update_or_create(component, account)
                component.update({'attrs': {'form_id': form_id}})
            LandingPageComponentServer.create(**component)

    @classmethod
    def brief_info(cls, **query_info):
        landing_page_qs = LandingPage.search(**query_info).exclude(status=LandingPage.Status.DELETE).exclude(
            status=LandingPage.Status.DELETE).order_by(
            '-create_time')
        return landing_page_qs

    @classmethod
    def publish(cls, landing_page_id):
        landing_page = cls.get_landing_page_by_id(landing_page_id)
        if landing_page.status not in (LandingPage.Status.UNPUBLISHED, LandingPage.Status.SUSPEND):
            raise BusinessError('投放页状态异常，无法发布')
        from django.conf import settings
        actual_url = "{d}/show/showpage?id={u}".format(d=settings.HOST_DOMAIN_PUBLISH, u=landing_page.id)
        landing_page.update(status=LandingPage.Status.PUBLISHED, url=actual_url)
        return actual_url

    @classmethod
    def delete(cls, landing_page_id):
        cls.get_landing_page_by_id(landing_page_id).update(status=LandingPage.Status.DELETE)

    @classmethod
    def get_relative_form(cls, page_id):
        # landing_page = cls.get_landing_page_by_id(page_id)
        customer_qs = CustomerServer.search(**{'landing_page_id': page_id})

        form_ids = list(set([customer.form_id for customer in customer_qs]))
        form_qs = Form.search(id__in=form_ids)

        # form_ids = set()
        # components = landing_page.landing_page_components.all()
        # for component in components:
        #     if component.c_type == LandingPageComponent.CType.FORM:
        #         form_ids.add(component.attrs.get('form_id'))
        # form_qs = Form.search(id__in=list(form_ids))
        return form_qs

    @classmethod
    def preview_landing_page_and_components(cls, landing_page_id):
        landing_page = LandingPage.get_byid(landing_page_id)
        if not landing_page:
            raise BusinessError('投放页不存在')

        components = landing_page.landing_page_components.all()
        for component in components:
            if component.c_type == LandingPageComponent.CType.FORM:
                form_id = component.attrs.get('form_id')
                form, form_components = FormServer.get_form_and_components(form_id)
                form_attrs = cls.render_form(form, form_components)
                component.attrs = form_attrs
        return landing_page, components
