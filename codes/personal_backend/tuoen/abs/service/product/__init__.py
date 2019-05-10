# coding=UTF-8

'''
Created on 2016年7月22日

@author: Administrator
'''

import hashlib
import datetime
import json
import random

from django.db.models import Q
from tuoen.sys.core.exception.business_error import BusinessError
from tuoen.sys.utils.common.split_page import Splitor

from model.models import ProductModel
from model.models import Product


class ProductOperateServer(object):
    @classmethod
    def add(cls, **attrs):
        """add new product"""
        if Product.query(name=attrs['name']):
            BusinessError("产品名称已存在")
        product = Product.create(**attrs)
        if not product:
            raise BusinessError("产品添加失败")

    @classmethod
    def update(cls, **attrs):
        """修改产品信息"""
        if 'name' in attrs:
            name = attrs['name']
            id_qs = [p.id for p in Product.query(name=name)]
            if id_qs and attrs['id'] not in id_qs:
                raise BusinessError("产品名称已存在")
        product = Product().update(**attrs)
        return product

    @classmethod
    def search(cls, current_page, **search_info):
        """查询产品列表"""
        if 'keyword' in search_info:
            keyword = search_info.pop('keyword')
            product_qs = Product.search(**search_info).filter(Q(name__contains = keyword) | \
                            Q(id__contains = keyword))
        else:
            product_qs = Product.search(**search_info)
        product_qs = product_qs.order_by("-create_time")
        return Splitor(current_page, product_qs)

    @classmethod
    def remove(cls, **attrs):
        """移除产品型号"""
        id = attrs['id']
        Product.query(id=id).delete()
        return True

class ProductModelServer(object):
    @classmethod
    def add(cls, **attrs):
        """add new product model"""
        if ProductModel.query(name=attrs['name']):
            BusinessError("产品型号已存在")
        product_id = attrs['product']
        product = Product.get_byid(product_id)
        attrs.update({"product": product})
        product_model = ProductModel.create(**attrs)
        if not product_model:
            raise BusinessError("产品型号添加失败")

    @classmethod
    def update(cls, **attrs):
        """修改产品型号信息"""

        product = ProductModel.query(id=attrs['id'])[0].product
        attrs.update({'product': product})
        if 'name' in attrs:
            name = attrs['name']
            product__model_ids = [pm.id for pm in ProductModel.query(name=name)]
            if product__model_ids and attrs['id'] not in product__model_ids:
                raise BusinessError("产品型号已存在")
        product__model = ProductModel().update(**attrs)
        return product__model

    @classmethod
    def search(cls, **search_info):
        """"查询产品型号"""
        product_id = search_info.pop('id')
        product = Product.get_byid(product_id)
        product_model_qs = ProductModel.search(product=product)
        product_model_qs = product_model_qs.order_by("-create_time")
        return product_model_qs

    @classmethod
    def remove(cls, **attrs):
        """移除产品型号"""
        id = attrs['id']
        ProductModel.query(id=id).delete()
        return True