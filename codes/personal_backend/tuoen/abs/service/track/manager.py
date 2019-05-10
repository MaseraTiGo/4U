# coding=UTF-8

'''
Created on 2016年7月22日

@author: Administrator
'''

import hashlib
import datetime
import json
import random

from tuoen.sys.core.exception.business_error import BusinessError
from tuoen.sys.utils.common.split_page import Splitor

from model.store.model_track_event import TrackEvent


class TrackEventServer(object):

    @classmethod
    def generate(cls, **attr):
        """创建跟踪"""

        track_event = TrackEvent.create(**attr)

        if track_event is None:
            raise BusinessError("创建失败")

        return True

    @classmethod
    def search(cls, current_page, **search_info):
        """查询跟踪列表"""

        track_event_qs = TrackEvent.query(**search_info)

        track_event_qs.order_by("-create_time")
        return Splitor(current_page, track_event_qs)

    @classmethod
    def search_by_sale_chance(cls, sale_chance):
        """根据机会查询跟踪列表"""

        track_event_qs = TrackEvent.search(create_time__range = (sale_chance.create_time, sale_chance.end_time), customer = sale_chance.customer)
        track_event_qs = track_event_qs.order_by("-create_time")
        return track_event_qs[:5]

