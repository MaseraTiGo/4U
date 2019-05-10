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

from model.store.model_mobilephone import MobileDevices, Mobilephone


class MobileDevicesHelper(object):

    @classmethod
    def generate(cls, **attrs):
        """添加手机设备"""
        if 'code' in attrs:
            code = attrs['code']
            if MobileDevices.search(code=code).count()>0:
                raise  BusinessError('手机编码重复')
        mobiledevices = MobileDevices.create(**attrs)
        if mobiledevices is None:
            raise BusinessError("添加手机设备失败")

        return mobiledevices

    @classmethod
    def search(cls, current_page, **search_info):
        """查询手机设备列表"""
        mobile_devices_qs = cls.searchall(**search_info)
        return Splitor(current_page, mobile_devices_qs)

    @classmethod
    def searchall(cls, **search_info):
        """查询所有的手机设备列表"""
        mobile_devices_qs = MobileDevices.query(**search_info)
        mobile_devices_qs = mobile_devices_qs.order_by("-create_time")
        return mobile_devices_qs

    @classmethod
    def get(cls, mobile_devices_id):
        """获取手机设备详情"""
        mobile_devices = MobileDevices.get_byid(mobile_devices_id)
        if mobile_devices is None:
            raise BusinessError("此手机设备不存在")
        return mobile_devices

    @classmethod
    def update(cls, mobile_devices, **attrs):
        """修改手机设备信息"""
        mobile_devices.update(**attrs)

        return mobile_devices

    @classmethod
    def update_new(cls, id, **attrs):
        """修改手机设备信息"""
        if 'code' in attrs:
            code = attrs['code']
            code_rpt = Mobilephone.search(id=id)[0].devices.code
            if MobileDevices.search(code=code).count()>0 and code != code_rpt:
                raise  BusinessError('手机编码重复')
        mp = Mobilephone.search(id=id)
        if mp:
            try:
                mp[0].devices.update(**attrs)
            except Exception as e:
                raise  BusinessError("更新失败{e}")
                return False
        return True

    @classmethod
    def remove(cls, mobile_devices):
        """修改手机设备信息"""

        mobile_devices.delete()
        return True

    @classmethod
    def is_code_exist(cls, code, mobile_devices = None):
        """判断手机设备编号是否存在"""

        mobile_devices_qs = MobileDevices.search(code = code)
        if mobile_devices is not None:
            mobile_devices_qs = mobile_devices_qs.filter(~Q(id = mobile_devices.id))

        if mobile_devices_qs.count() > 0:
            raise BusinessError("该手机设备编号已存在")

        return True
