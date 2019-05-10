# coding=UTF-8

from tuoen.sys.core.api.base import BaseApi
from tuoen.sys.core.exception.debug_error import DebugError

from tuoen.abs.service.user.manager import UserServer, StaffServer


class NoAuthrizedApi(BaseApi):

    def authorized(self, request, parms):
        return parms


class AuthorizedApi(BaseApi):

    _user_id = None
    _auth_flag = "auth"

    def _check_IP(self, token):
        print('check ip ......')

    def _check_time(self, token):
        print('check api timeout ...')


class UserAuthorizedApi(AuthorizedApi):

    @property
    def auth_user(self):
        if not hasattr(self, "_auth_user"):
            self._auth_user = self.load_auth_user()
        return self._auth_user

    def authorized(self, request, parms):
        auth_str = parms.pop(self._auth_flag)
        token = UserServer.get_token(auth_str)
        self._user_id = token.user_id
        return parms

    def load_auth_user(self):
        raise NotImplementedError('Please imporlement this interface in subclass')


class StaffAuthorizedApi(UserAuthorizedApi):

    def load_auth_user(self):
        staff = StaffServer.get(self._user_id)
        staff = StaffServer.get_staff_security(staff)
        return staff
