# coding=UTF-8

from support.common.maker import BaseLoader


class AccountLoader(BaseLoader):

    def generate(self):
        return [{
            'username': 'admin',
            'name': 'admin',
            'phone': '00000000000',
        }]
