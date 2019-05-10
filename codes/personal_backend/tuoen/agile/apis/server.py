# coding=UTF-8
import hashlib

from tuoen.sys.core.exception.business_error import BusinessError

from tuoen.sys.core.api.base import BaseApi
from tuoen.sys.core.exception.debug_error import DebugError

from tuoen.abs.service.user.manager import UserServer, StaffServer
from tuoen.agile.apis.base import AuthorizedApi


class ServerAuthorizedApi(AuthorizedApi):

    _auth_token = "BQkhcGMXQDujIXpExAmPLe"

    def authorized(self, request, parms):
        return parms


class MiniAuthorizedApi(ServerAuthorizedApi):

    def authorized(self, request, parms):
        '''
        timestamp = parms["parms"]

        auth_str = "{token}{timestamp}".format(token = self._auth_token, timestamp = timestamp)

        if hashlib.md5(auth_str.encode("utf-8")).hexdigest() != parms["auth"]:
            raise BusinessError("验证失败")
        '''
        return parms
