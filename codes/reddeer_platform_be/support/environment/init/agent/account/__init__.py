# coding=UTF-8

from support.common.maker import BaseLoader


class AccountLoader(BaseLoader):

    def generate(self):
        return [{
            'username': 'black_deer',
            'name': '橙鹿教育',
            'phone': '11111111111',
            'is_main': True
        }]
