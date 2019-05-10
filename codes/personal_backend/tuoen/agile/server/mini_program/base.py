# coding=UTF-8

from tuoen.sys.core.service.base import BaseAPIService
from tuoen.abs.middleware.rule import rule_register, \
            permise_rules
from tuoen.abs.middleware.rule.constant import Permise, Shop

from tuoen.agile.apis import test


class MiniService(BaseAPIService):

    @classmethod
    def get_name(self):
        return "小程序服务"

    @classmethod
    def get_desc(self):
        return "提供小程序服务"

    @classmethod
    def get_flag(cls):
        return "mini"

mini_service = MiniService()

from tuoen.agile.apis.mini.order import Search
mini_service.add(Search)

from tuoen.agile.apis.mini.transaction import Search
mini_service.add(Search)
