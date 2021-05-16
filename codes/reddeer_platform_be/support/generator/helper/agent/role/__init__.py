# coding=UTF-8

from tuoen.sys.utils.common.dictwrapper import DictWrapper
from model.store.model_role import AgentRole
from support.generator.helper.agent.company import CompanyGenerator
from support.generator.base import BaseGenerator


class AgentRoleGenerator(BaseGenerator):

    def __init__(self, agent_role_info):
        super(AgentRoleGenerator, self).__init__()
        self._agent_role_infos = self.init(agent_role_info)

    def get_create_list(self, result_mapping):
        company_list = result_mapping.get(CompanyGenerator.get_key())
        agent_role_list = []
        for company in company_list:
            for role_info in self._agent_role_infos:
                role = role_info.copy()
                role.update({
                    'company': company
                })
                agent_role_list.append(DictWrapper(role))
        return agent_role_list

    def create(self, agent_role_info, result_mapping):
        agent_role_qs = AgentRole.search(
            name=agent_role_info.name,
            company=agent_role_info.company
        )
        if agent_role_qs.count():
            agent_role = agent_role_qs[0]
        else:
            agent_role = AgentRole.create(**agent_role_info)
        return agent_role

    def delete(self):
        print('======================>>> delete agent_role <======================')
        return None
