# -*- coding: UTF-8 -*-
# Author: Dongjd
# FileName: __init__.py
# DateTime: 2020/12/15 15:18
# Project: awesome_dong
# Do Not Touch Me!

import datetime
from copy import deepcopy

from model.store.model_component import LandingPageComponent
from model.store.model_landingpage import LandingPage
from model.store.model_forms import Form
from model.store.model_landingpagevent import FormEvent
from model.store.utils import generate_uuid
from tuoen.abs.agent_service.component.manager import FormComponentServer
from tuoen.abs.agent_service.event.manager import FormEventServer
from tuoen.sys.core.exception.business_error import BusinessError
from tuoen.sys.utils.common.split_page import Splitor
from tuoen.abs.agent_service.customer.manager import CustomerServer


class FormServer(object):

    @classmethod
    def list(cls, **default_query_info):
        from_qs = Form.search(**default_query_info).exclude(is_delete=True).order_by('-create_time')
        return from_qs

    @classmethod
    def create(cls, **create_info):
        components = None
        if 'components' in create_info:
            components = create_info.pop('components')
        form = Form.create(**create_info)
        if form and components:
            FormComponentServer.bulk_create(form, components)
        from django.conf import settings
        actual_url = "{d}/show/showform/?id={u}".format(d=settings.HOST_DOMAIN_PUBLISH, u=form.id)
        if not form.url:
            form.update(url=actual_url)
        return form

    @classmethod
    def soft_delete(cls, form_id):
        form = Form.search(id=form_id).first()
        form.update(is_delete=True)
        return form

    @classmethod
    def add_landing_page_accord_to_id(cls, unique_id, landing_page):
        form = Form.search(unique_id=unique_id).first()
        if not form:
            raise BusinessError('form不存在!')
        if form.is_delete:
            raise BusinessError('关联的form已弃用！')
        form.landing_pages.add(landing_page)

    @classmethod
    def query(cls, **query_info):
        form_qs = Form.search(**query_info).exclude(is_delete=True).order_by('-create_time')
        return form_qs

    @classmethod
    def hung_landing_page_nums(cls, forms):
        for form in forms.data:
            search_info = {
                'attrs__form_id': form.id,
                'landing_page__status__in': [LandingPage.Status.PUBLISHED, LandingPage.Status.SUSPEND,
                                             LandingPage.Status.UNPUBLISHED]
            }
            # form.landing_pages_num = form.landing_pages.all().count()
            form.landing_pages_num = len(
                set([lpc.landing_page_id for lpc in LandingPageComponent.search(**search_info)]))

    @classmethod
    def hung_feedback_num_and_latest_time(cls, forms):
        for form in forms.data:
            collection_qs = form.form_customers.all().order_by('-create_time')
            form.latest_feedback = datetime.datetime.now()
            form.feedback_num = 0

            if collection_qs:
                form.latest_feedback = collection_qs[0].create_time
                form.feedback_num = collection_qs.count()

    @classmethod
    def hung_account(cls, forms):
        form_events = FormEvent.search(**{'form__in': forms.data})
        f_e_mapping = {f_e.form.id: f_e for f_e in form_events}
        for form in forms.data:
            form.account = None
            if f_e_mapping.get(form.id):
                form.account = f_e_mapping.get(form.id).account

    @classmethod
    def hung_landing_page_ids(cls, forms):
        for form in forms.data:
            lpc_qs = LandingPageComponent.objects.filter(attrs__form_id=form.id)
            lp_ids = [lpc.landing_page.id for lpc in lpc_qs]
            form.landing_page_ids = lp_ids

    @classmethod
    def get_n_page(cls, current_page, **query_info):
        if 'keywords' in query_info:
            keywords = query_info.pop('keywords')
            query_info.update({'name__icontains': keywords})
        form_qs = cls.query(**query_info)
        forms = Splitor(current_page, form_qs, size=20)
        cls.hung_landing_page_nums(forms)
        cls.hung_feedback_num_and_latest_time(forms)
        cls.hung_account(forms)
        # cls.hung_landing_page_ids(forms)
        return forms

    @classmethod
    def rename(cls, form_id, new_name):
        form = Form.search(id=form_id).first()
        form.name = new_name
        form.save()
        return form

    @classmethod
    def make_fucking_copy_by_id(cls, form_id, copy_name):
        form = Form.search(id=form_id).first()
        components = form.form_components.all()
        now = datetime.datetime.now()
        form.pk = None
        form.name = copy_name
        form.unique_id = generate_uuid(Form.PREFIX)
        form.create_time = now
        form.save()
        from django.conf import settings
        actual_url = "{d}/show/showform?id={u}".format(d=settings.HOST_DOMAIN_PUBLISH, u=form.id)
        form.update(url=actual_url)
        for component in components:
            component.pk = None
            component.form = form
            component.create_time = now
            component.save()
        return form

    @classmethod
    def get_form_and_components(cls, form_id):
        form = Form.search(id=form_id).first()
        components = form.form_components.all()
        return form, components

    @classmethod
    def multi_get_form_and_components(cls, form_ids):
        form_ids = list(set(form_ids))
        forms_infos = []
        form_qs = Form.search(**{'id__in': form_ids}).order_by('-create_time')
        if form_qs.count() != len(form_ids):
            db_ids = set([form.id for form in form_qs])
            x_ids = set(form_ids) - db_ids
            raise BusinessError('form不存在')
        for form in form_qs:
            components = form.form_components.all()
            forms_infos.append((form, components))
        return forms_infos

    @classmethod
    def get_company_by_id(cls, form_id):
        form = Form.search(id=form_id).first()
        if not form:
            raise BusinessError('表单不存在')
        return form.company

    @classmethod
    def get_form_by_id(cls, form_id):
        form = Form.search(id=form_id).first()
        if not form:
            raise BusinessError('form不存在')
        return form

    @classmethod
    def publish(cls, form_id):
        form = cls.get_form_by_id(form_id)
        if form.is_delete:
            raise BusinessError('投放页状态异常，无法发布')
        from django.conf import settings
        actual_url = "{d}/show/showform/?id={u}".format(d=settings.HOST_DOMAIN_PUBLISH, u=form.id)
        form.update(url=actual_url)
        return actual_url

    @classmethod
    def get_relative_landing_page(cls, form_id):
        customer_qs = CustomerServer.search(form_id=form_id)
        landing_page_ids = list(set([customer.landing_page_id for customer in customer_qs if customer.landing_page_id]))

        lp_qs = LandingPage.all_objects.filter(id__in=landing_page_ids)

        # lpc_qs = LandingPageComponent.objects.filter(attrs__form_id=form_id)
        # lp_qs = set([lpc.landing_page for lpc in lpc_qs if lpc.landing_page.status != LandingPage.Status.DELETE])
        return lp_qs

    @classmethod
    def edit(cls, **edit_info):
        form_id = edit_info.pop('id')
        form = cls.get_form_by_id(form_id)
        if not form:
            raise BusinessError('表单异常')
        components = None
        if 'components' in edit_info:
            components = edit_info.pop('components')

        form.form_components.all().delete()

        form.update(**edit_info)

        if components:
            FormComponentServer.bulk_create(form, components)

        return form

    @classmethod
    def is_form_changed(cls, form_info):
        components = form_info.pop('components')
        form = Form.search(**form_info).first()
        if not form:
            return True

        db_components_num = form.form_components.all().count()
        if db_components_num != len(components):
            return True

        for component in components:
            component.update({'form': form})
            cpt = FormComponentServer.search(**component)
            if not cpt:
                return True

        # has_id = [True for component in components if 'id' in component]
        # change_flag = all(has_id)
        # if not change_flag:
        #     return True
        return False

    @classmethod
    def update_or_create(cls, component, account):
        form_info = component.pop('attrs').pop('rightArr')
        form_info.update({'company': account.company})
        if 'id' in form_info:
            form_id = form_info['id']
            form_info_copy = deepcopy(form_info)
            is_form_changed = cls.is_form_changed(form_info_copy)
            if is_form_changed:
                form_info.pop('id')
                form = FormServer.create(**form_info)
                FormEventServer.create(
                    **{'account': account, 'action': FormEvent.ActionTypes.CREATE, 'form': form})
                form_id = form.id
        else:
            form = FormServer.create(**form_info)
            FormEventServer.create(
                **{'account': account, 'action': FormEvent.ActionTypes.CREATE, 'form': form})
            form_id = form.id
        return form_id
