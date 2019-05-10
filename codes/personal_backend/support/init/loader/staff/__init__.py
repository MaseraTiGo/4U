# coding=UTF-8

import datetime
from model.models import GenderTypes
from support.init.base import BaseLoader


class StaffLoader(BaseLoader):

    def load(self):
        return [{
            'identity': '000000000000000000',
            'name': 'admin',
            'gender': GenderTypes.MAN,
            'birthday': datetime.datetime(2018, 6, 1),
            'number': 'BQ10001',
            'phone': '00000000000',
            'email': '000000000@qq.com',
            'address': '中国',
            'emergency_contact': '管理员',
            'emergency_phone': '00000000000',
            'entry_time': datetime.datetime(1949, 10, 1),
            'education': 'doctor',
            'bank_number': '0000 0000 0000 0000 000',
            'bank_name': '中国银行',
            'contract_b': '00000000',
            'contract_l': '00000000',
            'expire_time': datetime.datetime(2949, 10, 1),
            'is_working': True,
            'is_admin': True,
        }]
