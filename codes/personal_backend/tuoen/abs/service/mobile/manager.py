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

from tuoen.abs.service.mobile.devices import MobileDevicesHelper
from tuoen.abs.service.mobile.phone import MobilephoneHelper
from tuoen.abs.service.mobile.maintain import MobileMaintainHelper
from model.store.model_mobilephone import MobileMaintain

class MobileDevicesServer(object):

    @classmethod
    def generate(cls, **attrs):
        """添加手机设备"""
        mobiledevices = MobileDevicesHelper.generate(**attrs)
        return mobiledevices

    @classmethod
    def search(cls, current_page, **search_info):
        """查询手机设备列表"""
        return MobileDevicesHelper.search(current_page, **search_info)

    @classmethod
    def searchall(cls, **search_info):
        """查询手机设备所有列表"""
        return MobileDevicesHelper.searchall(**search_info)

    @classmethod
    def get(cls, mobile_devices_id):
        """获取手机设备详情"""
        return MobileDevicesHelper.get(mobile_devices_id)

    @classmethod
    def update(cls, mobile_devices, **attrs):
        """修改手机设备信息"""
        return MobileDevicesHelper.update(mobile_devices, **attrs)

    @classmethod
    def update_new(cls, id, **attrs):
        """修改手机设备信息"""
        return MobileDevicesHelper.update_new(id, **attrs)

    @classmethod
    def remove(cls, mobile_devices):
        """修改手机设备信息"""
        mobile_phone_qs = MobilephoneServer.searchall(devices = mobile_devices)
        if mobile_phone_qs.count() > 0:
            raise BusinessError("存在手机注册关系无法删除")

        mobile_maintain_qs = MobileMaintainServer.searchall(devices = mobile_devices)
        if mobile_maintain_qs.count() > 0:
            raise BusinessError("存在手机维护关系无法删除")

        return MobileDevicesHelper.remove(mobile_devices)

    @classmethod
    def is_code_exist(cls, code, mobile_devices = None):
        """判断手机设备编号是否存在"""
        return MobileDevicesHelper.is_code_exist(code, mobile_devices)

    @classmethod
    def hung_devices_byphone(cls, customer_list):
        """根据注册手机挂载手机设备编码"""
        mobile_devices_ids = [customer.mobiledevices.id \
                              for customer in customer_list]
        mobile_devices_mapping = {mobile_devices.id:mobile_devices for mobile_devices in \
                                  cls.searchall(id__in = mobile_devices_ids)}
        for customer in customer_list:
            if customer.mobiledevices.id is not None:
                mobile_devices = mobile_devices_mapping.get(customer.mobiledevices.id)
                customer.mobile_devices = mobile_devices

        return customer_list

class MobilephoneServer(object):

    @classmethod
    def generate(cls, **attrs):
        """添加手机"""
        return MobilephoneHelper.generate(**attrs)

    @classmethod
    def get(cls, mobile_phone_id):
        """查询手机信息"""
        return MobilephoneHelper.get(mobile_phone_id)

    @classmethod
    def update(cls, mobile_phone, **attrs):
        """修改手机信息"""
        return MobilephoneHelper.update(mobile_phone, **attrs)

    @classmethod
    def update_new(cls, id, **attrs):
        return MobilephoneHelper.update_new(id, **attrs)

    @classmethod
    def search(cls, current_page, **search_info):
        """查询手机列表"""
        return MobilephoneHelper.search(current_page, **search_info)

    @classmethod
    def searchall(cls, **search_info):
        """查询手机列表"""
        return MobilephoneHelper.search_qs(**search_info)

    @classmethod
    def remove(cls, mobile_phone_id):
        """删除手机"""
        return MobilephoneHelper.remove(mobile_phone_id)

    @classmethod
    def is_phone_exist(cls, phone, mobilephone = None):
        """判断手机号是否存在"""
        return MobilephoneHelper.is_phone_exist(phone, mobilephone)

    @classmethod
    def remove_all(cls, mobile_phone_id):
        return MobilephoneHelper.remove_all(mobile_phone_id)

    @classmethod
    def search_new(cls, current_page, **search_info):
        return MobilephoneHelper.search_new(current_page, **search_info)

    # @classmethod
    # def hung_leader_staff(cls, phone_qs):
    #     """挂载leader&staff"""
    #     import re
    #     for pq in phone_qs:
    #         pq.leader = None
    #         pq.staff_name = None
    #         mm = MobileMaintain.search(devices=pq.devices)
    #         if mm:
    #             pq.staff_name = mm[0].staff.name
    #             remark = mm[0].remark
    #             leader = re.search('leader:(\w+);', remark)
    #             if leader:
    #                 pq.leader = leader.groups()[0]


class MobileMaintainServer(object):

    @classmethod
    def generate(cls, **attrs):
        """添加手机设备维护关系"""
        return MobileMaintainHelper.generate(**attrs)

    @classmethod
    def get(cls, mobile_maintain_id):
        """查询手机设备维护信息"""
        return MobileMaintainHelper.get(mobile_maintain_id)

    @classmethod
    def update(cls, mobile_maintain, **attrs):
        """修改手机信息"""
        return MobileMaintainHelper.update(mobile_maintain, **attrs)

    @classmethod
    def search(cls, current_page, **search_info):
        """查询手机列表"""
        return MobileMaintainHelper.search(current_page, **search_info)

    @classmethod
    def searchall(cls, **search_info):
        """查询手机列表"""
        return MobileMaintainHelper.searchall(**search_info)

    @classmethod
    def remove(cls, mobile_maintain_id):
        """删除手机"""
        return MobileMaintainHelper.remove(mobile_maintain_id)

    @classmethod
    def is_maintain_exist(cls, mobile_devices, mobile_maintain = None):
        """判断此手机设备是否被绑定"""
        return MobileMaintainHelper.is_maintain_exist(mobile_devices, mobile_maintain)
