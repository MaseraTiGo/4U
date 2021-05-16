# coding=UTF-8

from tuoen.agile.base import AuthorizedApi


class ServerAuthorizedApi(AuthorizedApi):
    _auth_token = "BQkhcGMXQDujIXpExAmPLe"

    def authorized(self, request, parms):
        return parms

