# coding=UTF-8

import hashlib
import random
from support.generator.base import BaseGenerator
from support.generator.helper.agent.role import AgentRoleGenerator
from model.store.model_account import AgentAccount


class AgentAccountGenerator(BaseGenerator):

    def __init__(self, agent_account_info):
        super(AgentAccountGenerator, self).__init__()
        self._agent_account_infos = self.init(agent_account_info)

    def get_create_list(self, result_mapping):
        agent_role_list = result_mapping.get(AgentRoleGenerator.get_key())
        for agent_account_info in self._agent_account_infos:
            agent_account_info.role = 0
            agent_account_info.password = hashlib.md5("123456".encode('utf8')).hexdigest()
            role = random.choice(agent_role_list)
            agent_account_info.role = role
            agent_account_info.company = role.company
        return self._agent_account_infos

    def create(self, agent_account_info, result_mapping):
        agent_account_qs = AgentAccount.search(
            username=agent_account_info.username
        )
        if agent_account_qs.count():
            agent_account = agent_account_qs[0]
        else:
            agent_account = AgentAccount.create(**agent_account_info)
        return agent_account

    def delete(self):
        print('==================>>> delete agent_account <======================')
        return None
