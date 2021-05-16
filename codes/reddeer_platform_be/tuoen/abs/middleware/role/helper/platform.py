# coding=UTF-8

from tuoen.abs.middleware.role.helper.base import BaseRole
from model.store.model_role import PlatformRole


class PlatformRoleHelper(BaseRole):

    @staticmethod
    def get_role_model():
        return PlatformRole
