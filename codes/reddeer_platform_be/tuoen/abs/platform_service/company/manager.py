# -*- coding: UTF-8 -*-    
# Author: Dongjd
# FileName: manager
# DateTime: 2020/12/17 18:09
# Project: awesome_dong
# Do Not Touch Me!

from model.store.model_company import Company
from tuoen.sys.core.exception.business_error import BusinessError


class CompanyServer(object):
    @classmethod
    def create(cls, **create_info):
        return Company.create(**create_info)

    @classmethod
    def get_company_by_unique_id(cls, unique_id):
        return Company.search(unique_id=unique_id).first()

    @classmethod
    def get_company_by_name(cls, name):
        return Company.search(name=name).first()

    @classmethod
    def create_while_initial(cls, **initial_info):
        create_info = {}
        name = initial_info.pop('company_name')
        company = cls.get_company_by_name(name)
        if company and company.status != Company.ComStatus.DELETE:
            raise BusinessError('该名字机构已存在')
        create_info['name'] = name
        if 'company_phone' in initial_info:
            create_info['phone'] = initial_info.pop('company_phone')
        if 'company_address' in initial_info:
            create_info['address'] = initial_info.pop('company_address')
        return Company.create(**create_info)

    @classmethod
    def update(cls, company, **update_info):
        if "name" in update_info:
            company_o = cls.get_company_by_name(update_info["name"])
            if company_o and company_o.id != company.id and company_o.status != Company.ComStatus.DELETE:
                raise BusinessError("该机构名称重复")
        company.update(**update_info)
