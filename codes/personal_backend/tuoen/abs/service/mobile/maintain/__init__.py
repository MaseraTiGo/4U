# coding=UTF-8

'''
Created on 2016年7月22日

@author: Administrator
'''

import hashlib
import datetime
import json
import random

from django.db.models import *

from tuoen.sys.core.exception.business_error import BusinessError
from tuoen.sys.utils.common.split_page import Splitor

from model.store.model_mobilephone import MobileMaintain


class MobileMaintainHelper(object):

    @classmethod
    def generate(cls, **attrs):
        """添加手机设备维护"""
        mobilemaintain = MobileMaintain.create(**attrs)
        if mobilemaintain is None:
            raise BusinessError("添加手机设备维护失败")

        return mobilemaintain

    @classmethod
    def search(cls, current_page, **search_info):
        """查询手机设备维护列表"""

        keyword = ""
        if 'keyword' in search_info:
            keyword = search_info.pop('keyword')

        mobile_maintain_qs = cls.searchall(**search_info)

        if keyword:
            mobile_maintain_qs = mobile_maintain_qs.filter(Q(staff__name__contains = keyword) | \
                Q(devices__code__contains = keyword))

        mobile_maintain_qs = mobile_maintain_qs.order_by("-create_time")

        return Splitor(current_page, mobile_maintain_qs)

    @classmethod
    def searchall(cls, **search_info):
        """查询所有的手机设备维护列表"""
        mobile_maintain_qs = MobileMaintain.search(**search_info)
        return mobile_maintain_qs

    @classmethod
    def get(cls, mobile_maintain_id):
        """获取手机设备维护详情"""
        mobile_maintain = MobileMaintain.get_byid(mobile_maintain_id)
        if mobile_maintain is None:
            raise BusinessError("此手机设备维护不存在")
        return mobile_maintain

    @classmethod
    def update(cls, mobile_maintain, **attrs):
        """修改手机设备维护信息"""
        mobile_maintain.update(**attrs)

        return mobile_maintain

    @classmethod
    def remove(cls, mobile_maintain_id):
        """修改手机设备维护信息"""

        mobile_maintain = cls.get(mobile_maintain_id)
        mobile_maintain.delete()
        return True

    @classmethod
    def is_maintain_exist(cls, mobile_devices, mobile_maintain = None):
        """判断此手机设备是否被绑定"""

        mobile_maintain_qs = MobileMaintain.search(devices = mobile_devices)

        if mobile_maintain is not None:
            mobile_maintain_qs = mobile_maintain_qs.filter(~Q(id = mobile_maintain.id))

        if mobile_maintain_qs.count() > 0:
            raise BusinessError("该手机设备已被绑定")

        return True
