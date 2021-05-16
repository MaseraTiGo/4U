# coding=UTF-8

import json
from tuoen.abs.middleware.rule.constant import permise_rules, config_rules
from tuoen.abs.middleware.rule.entity import RuleEntity
from tuoen.sys.utils.common.single import Single

from tuoen.sys.utils.cache.redis import redis


class RuleRegister(Single):

    def __init__(self):
        self._rule_mapping = {}
        self._root_list = []

    def register_module(self, module, *modules):
        module_list = [module]
        module_list.extend(modules)
        for module_entity in module_list:
            mapping = module_entity.get_all_mapping()
            if module_entity.root.all_key not in self._rule_mapping:
                self._root_list.append(module_entity.root)
                self._rule_mapping.update(mapping)

    def get_roots(self):
        return self._root_list

    def get_rule_mapping(self):
        return self._rule_mapping

    def register_api(self, entity, api, *apis):
        entity.add_apis(api, *apis)


rule_register = RuleRegister()
rule_register.register_module(permise_rules)
rule_register.register_module(config_rules)


class RuleMiddleware(Single):

    redis_key_prefix = 'account_rules_'

    def __init__(self):
        self._rules = []

    @classmethod
    def store_2_redis(cls, tag, rules):
        redis.set(cls.redis_key_prefix + tag, rules)

    @classmethod
    def has_value(cls, tag, value):

        res = redis.get(cls.redis_key_prefix + tag)
        if res is None:
            return False
        else:
            return value in json.loads(res)
