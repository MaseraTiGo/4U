# -*- coding: utf-8 -*-
# file_name       : authentication.py
# file_func       :
# file_author     : 'Johnathan.Wick'
# file_create_date: 2020/9/5 10:32

from rest_framework.authentication import BasicAuthentication
from rest_framework.exceptions import AuthenticationFailed

from user_info.data_processor import verify_current_account


def generate_token():
    ...


class UserAuthenticator(BasicAuthentication):
    def authenticate(self, request):
        user, password = request.data.get('user'), request.data.get('password')
        return user, password
        # res = None
        # if all([user, password]):
        #     res = verify_current_account(user, password)
        # if res:
        #     return user, generate_token()
        # raise AuthenticationFailed('current username does not match password')
