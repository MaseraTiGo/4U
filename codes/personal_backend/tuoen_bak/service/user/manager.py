# coding=UTF-8

'''
Created on 2016年7月22日

@author: Administrator
'''

import hashlib
import datetime
import json
import random

from tuoen.utils.exception.business_error import BusinessError

from tuoen.service.user.token import Token
from model.models import User, Customer


class UserServer(object):

    @classmethod
    def login(cls, account, password):
        user = User.get_user_byaccount(account, password)
        if user is not None:
            return user, Token(user)
        else:
            return None, None

    @classmethod
    def create(cls, account, phone, verify_code, passwd, role_type,\
                 plat_type, source):
        user = User.create(account=account, phone=phone, passwd=passwd,\
                    role_type=role_type, plat_type=plat_type,\
                        source=source)
        if user:
            return user
        raise Exception("register user error")

    @classmethod
    def make_token(cls, user):
        return Token(user)

    @classmethod
    def get_token(cls, auth_token):
        return Token.get_token(auth_token)

class CustomerServer(object):

    @classmethod
    def register(cls, phone, verify_code, passwd, role_type,\
                 plat_type, source, **other_infos):
        user = UserServer.create(account=phone, phone=phone,\
                verify_code=verify_code, passwd=passwd,\
                    role_type=role_type, plat_type=plat_type,\
                        source=source)
        customer = Customer.create(user=user, **other_infos)
        return customer, user

