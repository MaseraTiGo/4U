# -*- coding: UTF-8 -*-    
# Author: Dongjd
# FileName: helper
# DateTime: 2/3/2021 10:18 AM
# Project: awesome_dong
# Do Not Touch Me!

import time

from model.store.model_collections import Collections
from model.store.model_component import FormComponent
from model.store.model_landingpage import LandingPage
from tuoen.abs.agent_service.collection.templates.base import BaseZipTemplate
from tuoen.abs.agent_service.component.helper import AgeParser, CommonParser, GenderParser
from tuoen.abs.agent_service.customer.manager import CustomerServer
from tuoen.abs.agent_service.form.manager import FormServer
from tuoen.abs.agent_service.landingpage.manager import LandingPageServer
from tuoen.sys.core.exception.business_error import BusinessError


class CollectionInfoParser(object):
    ComponentParsers = [AgeParser, CommonParser, GenderParser]

    def __init__(self, detail_data, source='p'):
        self._detail_data = detail_data
        self._source = source

    @property
    def form_components(self):

        forms = self._detail_data.get('detail_data', {}).get('form_data', [])

        form_cpts_mapping = {FormServer.get_form_by_id(form.get('id')): form.get('collections', []) for form in forms}
        return form_cpts_mapping

    @property
    def customer_initial_info(self):
        customer_info = {}
        if self._source == 'p':
            landing_page_id = self._detail_data.get('landing_page_id')
            landing_page = LandingPageServer.get_landing_page_by_id(landing_page_id)
            if landing_page.status != LandingPage.Status.PUBLISHED:
                raise BusinessError('投放页状态异常！')
            customer_info = {'landing_page': landing_page, 'company': landing_page.company}

        all_customer = []
        for form, components in self.form_components.items():
            if form.is_delete and self._source == 'f':
                raise BusinessError('表单状态异常')
            temp_customer_info = dict()
            temp_customer_info.update(customer_info)
            temp_customer_info.update({'form': form, 'company': form.company})
            for component in components:
                parsers = [cp(component) for cp in self.ComponentParsers]
                for parser in parsers:
                    if parser.parsed_data is not None:
                        temp_customer_info[
                            CustomerServer.customer_basic_info[component.get('tag')]] = parser.parsed_data
                        break
            all_customer.append(temp_customer_info)

        return all_customer

    @property
    def collection_initial_info(self):
        collection_infos = []
        for form in self._detail_data.get('detail_data', {}).get('form_data', []):
            collection_infos.append({'detail_data': {'form_data': [form]}})
        return collection_infos


class ExportHelper(object):
    DEFAULT_WAIT_TIME = 30 * 10_000
    DEFAULT_INTERVAL = 0.2

    @classmethod
    def pre_process_export_data(cls, query_info, pics=False):
        from orderedset import OrderedSet
        headers = OrderedSet()

        normal_tags = [FormComponent.Tag.NAME, FormComponent.Tag.PHONE, FormComponent.Tag.AGE,
                       FormComponent.Tag.ADDR, FormComponent.Tag.TEXT]

        def parse_detail_data(components):
            detail_info_dict = {}
            for cpt in components.popitem()[-1]:
                if cpt.get('tag') in normal_tags:
                    detail_info_dict[cpt.get('name')] = cpt.get('value')
                    headers.add(cpt.get('name'))
                if cpt.get('tag') == FormComponent.Tag.PICS and pics:
                    pic_info = cpt.get('imgObj')
                    pic_info['imgName'] = cpt.get('name') + '.' + pic_info['imgName'].split('.')[-1]
                    pic_info.update({'url': cpt.get('value'), 'type': 'pic'})
                    detail_info_dict[cpt.get('name')] = pic_info
                if cpt.get('tag') == FormComponent.Tag.ATTACH and pics:
                    attach_info = cpt.get('fileObj')
                    attach_info['fileName'] = cpt.get('name') + '.' + attach_info['fileName'].split('.')[-1]
                    attach_info.update({'url': cpt.get('value'), 'type': 'attach'})
                    detail_info_dict[cpt.get('name')] = attach_info
                if cpt.get('type') == FormComponent.CType.RADIO:
                    detail_info_dict[cpt.get('name')] = cpt.get('list')[0].get('label') if cpt.get('list') else '-'
                    headers.add(cpt.get('name'))
                if cpt.get('type') in [FormComponent.CType.CHECKBOX]:
                    values = []
                    for i in cpt.get('list', []):
                        values.append(i.get('label', ''))
                    detail_info_dict[cpt.get('name', 'unknown')] = '\n'.join(values)
                    headers.add(cpt.get('name'))
            return detail_info_dict

        if 'start_time' in query_info:
            s_time = query_info.pop('start_time')
            e_time = query_info.pop('end_time')
            query_info.update({
                'create_time__gte': s_time,
                'create_time__lte': e_time
            })

        customer_qs = CustomerServer.search(**query_info).order_by('-create_time')

        collection_qs = Collections.search(**{'customer__in': customer_qs})
        collection_mapping = {clt.customer.id: clt for clt in collection_qs}
        for customer in customer_qs:
            flag = 'p' if customer.landing_page else 'f'
            parser = CollectionInfoParser({'detail_data': collection_mapping.get(customer.id).detail_data}, source=flag)
            customer.detail_data = parse_detail_data(parser.form_components)
        return customer_qs, headers

    @classmethod
    def get_info_2_generate_excel(cls, query_info):
        prefix = ''
        classify = 'form'
        num = 0
        if 'landing_page_id' in query_info:
            landing_page = LandingPageServer.get_landing_page_by_id(query_info['landing_page_id'])
            prefix = landing_page.name
            classify = 'page'
            num = query_info['landing_page_id']
        elif 'form_id' in query_info:
            form = FormServer.get_form_by_id(query_info['form_id'])
            prefix = form.name
            num = query_info['form_id']

        company = query_info.get('company')
        if not company:
            raise BusinessError('账号机构信息异常')
        company_name = company.name if company.name else 'default'
        return [prefix, company_name, classify, num]

    @classmethod
    def generate_attach_zip(cls, customer_qs, sub_export_type, external=None, base_path=None):
        external.append(customer_qs)
        export = BaseZipTemplate(*external, base_path=base_path)
        export.fuck_it(sub_export_type)

        cls.wait_url_feedback(export)

        return export

    @classmethod
    def generate_excel(cls, prefix, company_name, classify, num, customer_qs, headers, template_num, push=True,
                       mid=''):
        from .templates import templates_mapping

        Template = templates_mapping.get(template_num)
        export = Template(prefix, company_name, classify, num, customer_qs, headers, push=push, mid=mid)
        export.fuck_it()
        if push:
            cls.wait_url_feedback(export)
        return export

    @classmethod
    def wait_url_feedback(cls, export):
        for _ in range(int(cls.DEFAULT_WAIT_TIME / cls.DEFAULT_INTERVAL)):
            if export.url:
                break
            time.sleep(cls.DEFAULT_INTERVAL)
