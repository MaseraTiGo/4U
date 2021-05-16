# -*- coding: UTF-8 -*-    
# Author: Dongjd
# FileName: base
# DateTime: 2020/12/18 9:40
# Project: awesome_dong
# Do Not Touch Me!

import jwt
from django.conf import settings
from jwt.exceptions import DecodeError, ExpiredSignatureError

from tuoen.abs.middleware.role import role_middleware
from tuoen.sys.core.api.base import BaseApi
from tuoen.sys.core.exception.access_error import AccountForbiddenError, AccessLimitError
from tuoen.sys.core.exception.authorization_error import AuthorizationError
from tuoen.sys.core.exception.business_error import BusinessError


class NoAuthrizedApi(BaseApi):

    def authorized(self, request, parms):
        return parms

    def has_permission(self, account_id, api_code):
        return True


class AuthorizedApi(BaseApi):
    _user_id = None
    _auth_flag = "auth"

    def _check_IP(self, token):
        print('check ip ......')

    def _check_time(self, token):
        print('check api timeout ...')


class BaseAccountAuthorizedApi(AuthorizedApi):
    AccountServer = None
    FLAG = None
    FORBIDDEN_ACCOUNT = set()
    RULES = set()
    NEW_RULES = {}

    def __init__(self):
        super().__init__()
        self.account_id = None
        self.role_id = None
        self.is_main = None
        self.flag = None
        self.company_id = None

    @property
    def auth_account(self):
        if not hasattr(self, "_auth_account"):
            self._auth_account = self.load_auth_account()
        return self._auth_account

    @classmethod
    def is_forbidden(cls, account_id):
        if account_id in cls.FORBIDDEN_ACCOUNT:
            raise AccountForbiddenError('账户已被停用')

    def authorized(self, request, params):
        token = params.get('jwt_token')
        secret = settings.SECRET_KEY
        try:
            payload = jwt.decode(token, secret)
        except (DecodeError, ExpiredSignatureError) as e:
            raise AuthorizationError(AuthorizationError.desc + str(e))
        self.account_id = payload.get('account_id')
        if self.auth_account.status != self.AccountServer.AccountModel.Status.ENABLE:
            raise AccountForbiddenError('账户已被停用')
        self.role_id = payload.get('role_id')
        self.company_id = payload.get('company_id')
        self.is_main = payload.get('is_main')
        self.flag = payload.get('flag')

        # one's account is been forbidden after login in.
        self.is_forbidden(self.account_id)

        if self.flag != self.FLAG:
            raise BusinessError('ILLEGAL REQUEST!')
        if settings.PERMISSION_CHECK and not self.is_main:
            self.has_permission(params.get('api'))
        return params

    def has_permission(self, api):
        # todo dong: how to make sure the role is new.
        # bind new role to the account that already login in
        account = self.auth_account
        try:
            rules = role_middleware.get_redis(
                self.RoleServer.RoleModel.__name__.lower(),
                account.role_id,
            )
            if api not in rules:
                raise AccessLimitError('无操作权限')
        except Exception as e:
            print(e)
            raise AccessLimitError('无操作权限')
        '''
        if self.account_id in self.NEW_RULES:
            self.role_id = self.NEW_RULES[self.account_id]

        keys = [self.AccountServer.AccountModel.__name__.lower(), str(self.role_id)]
        if self.company_id:
            keys = [self.AccountServer.AccountModel.__name__.lower(), str(self.company_id), str(self.role_id)]
        role_store_key = '_'.join(keys)
        if not RuleMiddleware.has_value(role_store_key, api):
            raise AccessLimitError('无操作权限')
        '''

    def load_auth_account(self):
        account = self.AccountServer.get_account_by_id(self.account_id)
        return account
