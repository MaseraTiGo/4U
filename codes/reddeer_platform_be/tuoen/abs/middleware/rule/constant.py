# coding=UTF-8

from tuoen.abs.middleware.rule.base import BaseRule
from tuoen.abs.middleware.rule.entity import RuleEntity


class Action(object):
    ADD = ("add", "添加")
    DELETE = ("delete", "删除")
    EDIT = ("edit", "编辑")
    QUERY = ("query", "查询")


class Permise(BaseRule):
    DEFAULT = RuleEntity("permise", "权限管理")

    DEFAULT_ROLE = RuleEntity("role", "角色管理")
    DEFAULT_ROLE_QUERY = RuleEntity(*Action.QUERY)
    DEFAULT_ROLE_ADD = RuleEntity(*Action.ADD)
    DEFAULT_ROLE_EDIT = RuleEntity(*Action.EDIT)
    DEFAULT_ROLE_DEL = RuleEntity(*Action.DELETE)


class Config(BaseRule):
    DEFAULT = RuleEntity("Config", "配置管理")

    DEFAULT_CONFIG = RuleEntity("Config", "配置管理")
    DEFAULT_CONFIG_QUERY = RuleEntity(*Action.QUERY)
    DEFAULT_CONFIG_EDIT = RuleEntity(*Action.EDIT)


permise_rules = Permise()

config_rules = Config()
