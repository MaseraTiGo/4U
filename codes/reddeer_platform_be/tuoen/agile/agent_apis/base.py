# coding=UTF-8

from tuoen.abs.agent_service.account.manager import AgentAccountServer
from tuoen.abs.agent_service.role.manager import AgentRoleServer
from tuoen.agile.base import BaseAccountAuthorizedApi


class AgentAccountAuthorizedApi(BaseAccountAuthorizedApi):
    AccountServer = AgentAccountServer
    RoleServer = AgentRoleServer
    FLAG = 'user'
    FORBIDDEN_ACCOUNT = set()
    NEW_RULES = {}
