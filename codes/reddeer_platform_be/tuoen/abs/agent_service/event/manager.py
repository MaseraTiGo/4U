# -*- coding: UTF-8 -*-    
# Author: Dongjd
# FileName: manager
# DateTime: 2020/12/16 19:32
# Project: awesome_dong
# Do Not Touch Me!

from model.store.model_landingpagevent import LandingPageEvent, FormEvent


class EventServerBase(object):
    EventModel = None

    @classmethod
    def create(cls, **create_info):
        cls.EventModel.create(**create_info)


class FormEventServer(EventServerBase):
    EventModel = FormEvent


class LandingPageEventServer(EventServerBase):
    EventModel = LandingPageEvent
