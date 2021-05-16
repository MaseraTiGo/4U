# coding=UTF-8

from support.common.maker import BaseLoader


class CompanyLoader(BaseLoader):

    def generate(self):
        return [{
            'name': '橙鹿教育',
            'unique_id': 'agent_2020122300001',
            'address': '湖北省武汉市洪山区光谷软件园',
            'phone': '11111111111',
            'login_url': '',
        }]
