# coding=UTF-8

import json
from tuoen.sys.utils.common.dictwrapper import DictWrapper
from tuoen.sys.log.base import logger
from model.store.model_product import Product, ProductModel
from support.generator.base import BaseGenerator


class ProductGenerator(BaseGenerator):

    def __init__(self, product_info):
        super(ProductGenerator, self).__init__()
        self._product_infos = self.init(product_info)

    def get_create_list(self, result_mapping):
        return self._product_infos

    def create(self, product_info, result_mapping):
        product_qs = Product.query().filter(name = product_info.name)
        if product_qs.count():
            product = product_qs[0]
        else:
            product = Product.create(**product_info)
        return product

    def delete(self):
        print('======================>>> delete product <======================')
        return None


class ProductModelGenerator(BaseGenerator):

    def __init__(self, product_model_info):
        super(ProductModelGenerator, self).__init__()
        self._product_model_infos = self.init(product_model_info)

    def get_create_list(self, result_mapping):
        product_list = result_mapping.get(ProductGenerator.get_key())
        product_mapping = {product.name: product for product in product_list}

        for product_model_info in self._product_model_infos:
            product_model_info.product = product_mapping[product_model_info.product_name]

        return self._product_model_infos

    def create(self, product_model_info, result_mapping):
        product_model_qs = ProductModel.query().filter(\
               product = product_model_info.product, name = product_model_info.name)
        if product_model_qs.count():
            product_model = product_model_qs[0]
        else:
            product_model = ProductModel.create(**product_model_info)
        return product_model

    def delete(self):
        print('======================>>> delete product_model <======================')
        return None
