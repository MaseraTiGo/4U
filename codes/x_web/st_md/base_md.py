# -*- coding: utf-8 -*-
# @File    : base_md
# @Project : x_web
# @Time    : 2023/7/12 20:54
# once, I want 2 leave my name 2 the history
# sadly, I find that my hair gets pale
"""                     
                                      /             
 __.  , , , _  _   __ ______  _    __/  __ ____  _, 
(_/|_(_(_/_</_/_)_(_)/ / / <_</_  (_/_ (_)/ / <_(_)_
                                                 /| 
                                                |/  
"""
import abc

import pandas as pd
import streamlit as st

from super_dong.frame.utils import gen_text_input_box_by_attrs, \
    gen_page_input_box
from super_dong.frame.utils.query_tools import TearParts


class Operation:
    READ = 'READ'
    CREATE = 'CREATE'
    UPDATE = 'UPDATE'
    DELETE = 'DELETE'


OPERATION = [
    Operation.READ,
    Operation.CREATE,
    Operation.UPDATE,
    Operation.DELETE,
]


class ModelRepo(abc.ABC):
    _models = {}
    _op_mapping_method = {}

    operation = None
    # Model = None

    unique_attr = None

    create_input_attrs = None
    update_input_attrs = None

    update_specify_attr = unique_attr
    delete_specify_attr = unique_attr

    read_exhibit_attrs = None

    def __init_subclass__(cls, **kwargs):
        cls._models.update(
            {
                cls.get_model().__name__: cls
            }
        )
        cls.operation = OPERATION if cls.operation is None else cls.operation

    @classmethod
    @abc.abstractmethod
    def get_model(cls):
        """return None"""

    @classmethod
    def get_options(cls):
        return cls._models.keys()

    @classmethod
    def execute(cls, model: str, operation: str):
        _sub_cls = cls._models[model]  # type: ModelRepo
        if operation.startswith(Operation.CREATE):
            _sub_cls.create()
        elif operation.startswith(Operation.DELETE):
            _sub_cls.delete()
        elif operation.startswith(Operation.UPDATE):
            _sub_cls.update()
        elif operation.startswith(Operation.READ):
            _sub_cls.read()
        else:
            raise Exception(f"{model} not support {operation}")

    @classmethod
    def create(cls):
        create_info = gen_text_input_box_by_attrs(cls.create_input_attrs)
        if st.button("Create"):
            cls.create_helper(**create_info)

    @classmethod
    def create_helper(cls, **kwargs):
        cls.get_model().create(**kwargs)
        st.success(f"{cls.get_model().__name__} created successfully!")

    @classmethod
    def delete(cls):
        specify_info = gen_text_input_box_by_attrs([cls.delete_specify_attr])
        if st.button("Delete"):
            affiliate = cls.get_model().get(
                name=specify_info[cls.delete_specify_attr])
            affiliate.delete_instance()
            st.success(f"{cls.get_model().__name__} deleted successfully!")

    @classmethod
    def update(cls):
        update_info = gen_text_input_box_by_attrs(cls.update_input_attrs)
        if st.button("Update"):
            cls.update_helper(**update_info)

    @classmethod
    def update_helper(cls, **kwargs):
        affiliate = cls.get_model().get(name=kwargs[cls.update_specify_attr])
        for attr in cls.update_input_attrs:
            setattr(affiliate, attr, kwargs[attr])
        affiliate.save()
        st.success(f"{cls.get_model().__name__} updated successfully!")

    @classmethod
    def read(cls):
        page_info = gen_page_input_box()
        affiliates = cls.get_model().select()
        affiliates = TearParts(affiliates, cur_page=page_info.page_num,
                               size=page_info.page_size).data
        data = []
        for affiliate in affiliates:
            tmp = {}
            attr: str
            for attr in cls.read_exhibit_attrs:
                if '.' not in attr:
                    value = getattr(affiliate, attr, '-')
                else:
                    sub_attrs = attr.split('.')
                    value = affiliate
                    for s_attr in sub_attrs:
                        value = getattr(value, s_attr)
                tmp[attr.capitalize()] = value
            data.append(tmp)

        df = pd.DataFrame(data)
        # 将DataFrame的索引设置为1
        df.index += 1
        # 将表头设置为'No.'
        df.columns.name = 'No.'

        st.table(df)


class AffiliateModelManager(ModelRepo):
    unique_attr = 'name'

    create_input_attrs = ['name', 'url']
    update_input_attrs = ['url']

    read_exhibit_attrs = ['name', 'url']

    update_specify_attr = unique_attr
    delete_specify_attr = unique_attr

    @classmethod
    def get_model(cls):
        from super_dong.model_store.models.model_affiliate import Affiliate
        return Affiliate


class AffiliateAccountModelManager(ModelRepo):
    unique_attr = 'username'

    create_input_attrs = ['username', 'password', 'affiliate_name']
    update_input_attrs = create_input_attrs[1:]

    read_exhibit_attrs = ['username', 'password', 'affiliate.name']

    update_specify_attr = unique_attr
    delete_specify_attr = unique_attr

    @classmethod
    def create_helper(cls, **kwargs):
        model = cls.get_model()
        affiliate = AffiliateModelManager.get_model().get(
            name=kwargs['affiliate_name'])
        model.create(
            username=kwargs['username'],
            password=kwargs['password'],
            affiliate=affiliate
        )
        st.success("Affiliate account created successfully!")

    @classmethod
    def update_helper(cls, **kwargs):
        aa_model = cls.get_model()
        account = aa_model.get(username=kwargs['username'])
        affiliate = AffiliateModelManager.get_model().get(
            name=kwargs['affiliate_name'])
        account.affiliate = affiliate
        account.password = kwargs['password']
        account.save()
        st.success("Affiliate account updated successfully!")

    @classmethod
    def get_model(cls):
        from super_dong.model_store.models.model_affiliate import \
            AffiliateAccount
        return AffiliateAccount
