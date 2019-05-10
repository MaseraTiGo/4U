# coding=UTF-8

import datetime
from model.models import GenderTypes
from support.init.base import BaseLoader


class CustomerLoader(BaseLoader):

    def load(self):
        return [{
            'identity': '000000000000000000',
            'name': '系统客户',
            'gender': GenderTypes.MAN,
            'birthday': datetime.datetime.now(),
            'phone': '15527703115',
            'email': '237818280@qq.com',
            'city':'中国',
            'address': '中国',
        }]
