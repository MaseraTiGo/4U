# coding=UTF-8

import time

from tuoen.sys.utils.common.single import Single
from tuoen.abs.middleware.rule.entity import RuleEntity
from tuoen.abs.middleware.rule.constant import permise_rules, shop_rules, staff_rules, order_rules, \
                                               mobile_rules, customer_rules, sale_chance_rules, service_item_rules, \
                                               measure_rules, data_import_rules, product_rules


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
rule_register.register_module(staff_rules)
rule_register.register_module(order_rules)
rule_register.register_module(mobile_rules)
rule_register.register_module(customer_rules)
rule_register.register_module(sale_chance_rules)
rule_register.register_module(service_item_rules)
rule_register.register_module(shop_rules)
rule_register.register_module(measure_rules)
rule_register.register_module(data_import_rules)
rule_register.register_module(product_rules)
