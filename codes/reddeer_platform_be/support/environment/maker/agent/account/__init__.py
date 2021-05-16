# coding=UTF-8

from support.generator.helper.agent import *
from support.common.maker import BaseMaker


class AgentAccountMaker(BaseMaker):

    def __init__(self, company_info, account_info, role_info):
        self._company = CompanyGenerator(company_info)
        self._role = AgentRoleGenerator(role_info)
        self._account = AgentAccountGenerator(account_info)

    def generate_relate(self):
        self._company.add_outputs(self._role, self._account)
        self._account.add_inputs(self._role)
        return self._account
