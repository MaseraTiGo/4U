# coding=UTF-8

import json
import random
from tuoen.sys.utils.common.dictwrapper import DictWrapper
from tuoen.sys.log.base import logger
from model.store.model_mobilephone import MobileDevices, Mobilephone, MobileMaintain
from support.generator.base import BaseGenerator

class MobileDevicesGenerator(BaseGenerator):

    def __init__(self, mobiledevices_info):
        super(MobileDevicesGenerator, self).__init__()
        self._mobiledevices_infos = self.init(mobiledevices_info)

    def get_create_list(self, result_mapping):
        return self._mobiledevices_infos

    def create(self, mobiledevices_info, result_mapping):
        mobiledevices_qs = MobileDevices.query().filter(code = mobiledevices_info.code)
        if mobiledevices_qs.count():
            mobiledevices = mobiledevices_qs[0]
        else:
            mobiledevices = MobileDevices.create(**mobiledevices_info)
        return mobiledevices

    def delete(self):
        print('======================>>> delete mobiledevices <======================')
        return None


class MobilePhoneGenerator(BaseGenerator):

    def __init__(self, mobilephone_info):
        super(MobilePhoneGenerator, self).__init__()
        self._mobilephone_infos = self.init(mobilephone_info)

    def get_create_list(self, result_mapping):
        mobile_devices_list = result_mapping.get(MobileDevicesGenerator.get_key())
        for mobilephone in self._mobilephone_infos:
                mobilephone.code = mobile_devices_list[0]
        return self._mobilephone_infos

    def create(self, mobilephone_info, result_mapping):
        mobilephone_qs = Mobilephone.query().filter(phone_number = mobilephone_info.phone_number)
        if mobilephone_qs.count():
            mobilephone = mobilephone_qs[0]
        else:
            mobilephone = Mobilephone.create(**mobilephone_info)
        return mobilephone

    def delete(self):
        print('======================>>> delete mobilephone <======================')
        return None


class MobileMaintainGenerator(BaseGenerator):

    def __init__(self, mobilemaintain_info):
        super(MobileMaintainGenerator, self).__init__()
        self._mobilemaintain_infos = self.init(mobilemaintain_info)

    def get_create_list(self, result_mapping):
        mobile_devices_list = result_mapping.get(MobileDevicesGenerator.get_key())
        for mobilemaintain in self._mobilemaintain_infos:
                mobilemaintain.code = random.choice(mobile_devices_list)
        return self._mobilemaintain_infos

    def create(self, mobilemaintain_info, result_mapping):
        mobilemaintain_qs = MobileMaintain.query().filter(code = mobilemaintain_info.code)
        if mobilemaintain_qs.count():
            mobilemaintain = mobilemaintain_qs[0]
        else:
            mobilemaintain = MobileMaintain.create(**mobilemaintain_info)
        return mobilemaintain

    def delete(self):
        print('======================>>> delete mobilemaintain <======================')
        return None

