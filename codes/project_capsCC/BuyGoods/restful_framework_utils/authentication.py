# -*- coding: utf-8 -*-
# file_name       : authentication.py
# file_func       :
# file_author     : 'Johnathan.Wick'
# file_create_date: 2019/9/29 9:23
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed

from BuyGoods.models_store.members import Users


def generate_token(key, expire=60):
    """

    :param key:
    :param expire:
    :return:
    """
    ex_time = str(time.time() + expire)
    ex_time_bytes = ex_time.encode('utf-8')
    sha1_hex_str = hmac.new(key.encode('utf-8'), ex_time_bytes, 'sha1').hexdigest()
    token = ex_time + ':' + sha1_hex_str
    b64_token = base64.urlsafe_b64encode(token.encode('utf-8'))
    return b64_token.decode('utf-8')


def certify_token(key, token):
    """

    :param key:
    :param token:
    :return:
    """
    if not token:
        return False
    token_str = base64.urlsafe_b64decode(token).decode('utf-8')
    ex_time, sha1_str = token_str.split(':')
    if ex_time < str(time.time()):
        return False
    ce_token = hmac.new(key.encode('utf-8'), ex_time.encode('utf-8'), 'sha1').hexdigest()
    if ce_token == sha1_str:
        return True
    return False


class UserAuthentication(BaseAuthentication):
    def authenticate(self, request):
        user = request.query_params.get('username', None)
        print('in authentication current user is', user)
        if request.method == 'GET':
            token = request.query_params.get('token', None)
            if certify_token(user, token):
                return
            else:
                raise AuthenticationFailed('token is not right or expired')
        password = request.query_params.get('password', None)
        if user:
            user_obj = Users.objects.filter(username=user, password=password)
            print('user_is', user, user_obj, 'login success!')
            if user_obj:
                return user, user_obj
        raise AuthenticationFailed('user is not exist!')
