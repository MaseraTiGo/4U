# -*- coding: UTF-8 -*-
# Author: Dongjd
# FileName: __init__.py
# DateTime: 2020/12/15 15:18
# Project: awesome_dong
# Do Not Touch Me!

from tuoen.sys.core.exception.business_error import BusinessError

from model.store.model_component import LandingPageComponent, FormComponent


class LandingPageComponentServer(object):
    @classmethod
    def create(cls, **create_info):
        LandingPageComponent.create(**create_info)

    @classmethod
    def bulk_create(cls, landing_page, create_infos):
        create_objs = []
        for create_info in create_infos:
            create_info.update({
                'landing_page': landing_page
            })
            create_objs.append(LandingPageComponent(**create_info))
        LandingPageComponent.objects.bulk_create(create_objs)

    @classmethod
    def delete_by_id(cls, c_id):
        landing_component = LandingPageComponent.get_byid(c_id)
        if not landing_component:
            return
        landing_component.delete()

    @classmethod
    def update_by_id(cls, c_id, update_info):
        landing_component = LandingPageComponent.get_byid(c_id)
        if not landing_component:
            raise BusinessError('组件不存在')
        landing_component.update(**update_info)


class FormComponentServer(object):

    @classmethod
    def create(cls, **create_info):
        ...

    @classmethod
    def bulk_create(cls, form, create_infos):
        create_objs = []
        for create_info in create_infos:
            if 'id' in create_info:
                create_info.pop('id')
            create_info.update({
                'form': form
            })
            create_objs.append(FormComponent(**create_info))
        FormComponent.objects.bulk_create(create_objs)

    @classmethod
    def search(cls, **search_info):
        return FormComponent.search(**search_info).first()

