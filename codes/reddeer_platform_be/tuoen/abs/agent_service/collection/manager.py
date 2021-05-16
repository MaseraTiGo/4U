# -*- coding: UTF-8 -*-
# Author: Dongjd
# FileName: __init__.py
# DateTime: 2020/12/15 15:18
# Project: awesome_dong
# Do Not Touch Me!


from model.store.model_collections import Collections
from tuoen.abs.agent_service.collection import ExportType, AttachmentExportType
from tuoen.abs.agent_service.collection.helper import CollectionInfoParser
from tuoen.abs.agent_service.collection.helper import ExportHelper
from tuoen.abs.agent_service.customer.manager import CustomerServer
from tuoen.sys.core.exception.business_error import BusinessError
from tuoen.sys.utils.common.split_page import Splitor


class CollectionServer(object):

    @classmethod
    def get_n_page(cls, current_page, **search_info):
        customer_qs = CustomerServer.search(**search_info)
        collection_qs = Collections.search(**{'customer__in': customer_qs})
        collection_mapping = {clt.customer.id: clt for clt in collection_qs}
        for customer in customer_qs:
            customer.detail_data = collection_mapping.get(customer.id).detail_data
        valid_num = Collections.objects.filter(is_valid=True, customer__in=customer_qs).count()
        return Splitor(current_page, customer_qs, size=20), valid_num

    @classmethod
    def search(cls, order_by='-create_time', **search_info):
        collection_qs = Collections.search(**search_info).order_by(order_by)
        return collection_qs

    @classmethod
    def dispatch(cls, excel_template_num, export_type, sub_export_type, query_info=None):
        export = ''
        base_info = ExportHelper.get_info_2_generate_excel(query_info)
        if export_type == ExportType.EXCEL_ONLY:
            customer_qs, headers = ExportHelper.pre_process_export_data(query_info)
            base_info.extend([customer_qs, headers, excel_template_num])
            export = ExportHelper.generate_excel(*base_info)
        if export_type == ExportType.ATTACHMENT_ONLY:
            customer_qs, headers = ExportHelper.pre_process_export_data(query_info, pics=True)
            export = ExportHelper.generate_attach_zip(customer_qs, sub_export_type, external=base_info)
        if export_type == ExportType.EXCEL_AND_ATTACHMENT:
            customer_qs, headers = ExportHelper.pre_process_export_data(query_info, pics=True)
            from copy import deepcopy
            excel_info = deepcopy(base_info)
            excel_info.extend([customer_qs, headers, excel_template_num])
            base_path = ExportHelper.generate_excel(*excel_info, push=False).temp_path
            export = ExportHelper.generate_attach_zip(customer_qs, sub_export_type, external=base_info,
                                                      base_path=base_path)

        if not export or not export.url:
            raise BusinessError('export failed, contact Administrator 4 further information!')
        try:
            export.clear_up()
        except Exception as _:
            ...
        return export.url

    @classmethod
    def export_by_time_scope(cls, **query_info):

        from .templates.std_excel_template import StdExcelTemplate
        excel_template_num = query_info.pop(
            'template_num') if 'template_num' in query_info else StdExcelTemplate.UNIQUE_NUM
        export_type = query_info.pop('export_type') if 'export_type' in query_info else ExportType.EXCEL_ONLY
        if export_type not in ExportType.__members__.values():
            raise BusinessError('export type invalid！')

        sub_export_type = query_info.pop(
            'sub_export_type') if 'sub_export_type' in query_info else AttachmentExportType.BY_CUSTOMER
        if sub_export_type not in AttachmentExportType.__members__.values():
            raise BusinessError('sub export type invalid！')

        res_url = cls.dispatch(excel_template_num, export_type, sub_export_type, query_info)
        return res_url

    @classmethod
    def process_data(cls, source, **mixing_info):
        parser = CollectionInfoParser(mixing_info, source=source)
        customer_infos = parser.customer_initial_info
        customers = []
        for customer in customer_infos:
            customers.append(CustomerServer.create(**customer))

        collection_infos = parser.collection_initial_info
        for collection_info in collection_infos:
            for customer in customers:
                if customer.form.id == int(collection_info.get('detail_data', {}).get('form_data', [{}])[0].get('id')):
                    collection_info.update({'customer': customer})
                    break
        Collections.objects.bulk_create([Collections(**collection) for collection in collection_infos])
