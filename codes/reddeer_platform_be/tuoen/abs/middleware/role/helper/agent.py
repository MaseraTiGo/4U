# coding=UTF-8

from tuoen.abs.middleware.role.helper.base import BaseRole
from model.store.model_role import AgentRole


class AgentRoleHelper(BaseRole):

    @staticmethod
    def get_role_model():
        return AgentRole
