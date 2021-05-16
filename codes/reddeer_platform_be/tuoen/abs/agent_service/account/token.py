# coding=UTF-8

'''
Created on 2016年7月22日

@author: Administrator
'''

import datetime

import jwt
from django.conf import settings


class JwtGenerator(object):
    secret = settings.SECRET_KEY

    @classmethod
    def generate_jwt(cls, account):
        payload = {
            'flag': 'user',
            'account_id': account.id,
            'company_id': account.company.id,
            'role_id': account.role.id,
            'is_main': account.is_main,
            'exp': datetime.datetime.now() + datetime.timedelta(days=1),
        }
        return jwt.encode(payload=payload, key=cls.secret)
