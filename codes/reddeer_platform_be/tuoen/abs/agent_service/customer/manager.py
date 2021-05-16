# -*- coding: UTF-8 -*-    
# Author: Dongjd
# FileName: manager
# DateTime: 2020/12/24 17:45
# Project: awesome_dong
# Do Not Touch Me!


from model.store.model_customer import Customer


class CustomerServer(object):
    customer_basic_info = {0: 'name', 1: 'phone', 2: 'birthday', 3: 'gender', 4: 'placeholder', 5: 'placeholder2',
                           6: 'address', 7: 'placeholder3'}

    @classmethod
    def create(cls, **create_info):
        return Customer.create(**create_info)

    @classmethod
    def search(cls, **search_info):
        return Customer.search(**search_info).order_by('-create_time')
