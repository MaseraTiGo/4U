# coding=UTF-8

from model.store.model_company import Company
from support.generator.base import BaseGenerator


class CompanyGenerator(BaseGenerator):

    def __init__(self, company_info):
        super(CompanyGenerator, self).__init__()
        self._company_infos = self.init(company_info)

    def get_create_list(self, result_mapping):
        return self._company_infos

    def create(self, company_info, result_mapping):
        company_qs = Company.search(name=company_info.name)
        if company_qs.count():
            company = company_qs[0]
        else:
            company = Company.create(**company_info)
        return company

    def delete(self):
        print('======================>>> delete company <======================')
        return None
