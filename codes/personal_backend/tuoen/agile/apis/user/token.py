# coding=UTF-8

from tuoen.sys.core.exception.business_error import BusinessError
from tuoen.sys.core.field.base import CharField, DictField, IntField, ListField
from tuoen.sys.core.api.request import RequestField, RequestFieldSet
from tuoen.sys.core.api.utils import with_metaclass
from tuoen.sys.core.api.response import ResponseField, ResponseFieldSet

from tuoen.agile.apis.base import NoAuthrizedApi
from tuoen.abs.service.user.manager import UserServer


class Renew(NoAuthrizedApi):
    """续签token"""
    request = with_metaclass(RequestFieldSet)
    request.auth_token = RequestField(CharField, desc = "用户访问令牌")
    request.renew_flag = RequestField(CharField, desc = "续签访问令牌标识")

    response = with_metaclass(ResponseFieldSet)
    response.auth_token = ResponseField(CharField, desc = "用户访问令牌")
    response.renew_flag = ResponseField(CharField, desc = "续签访问令牌标识")

    @classmethod
    def get_desc(cls):
        return "续签访问令牌"

    @classmethod
    def get_author(cls):
        return "fsy"

    def execute(self, request):
        token = UserServer.renew_token(request.auth_token, request.renew_flag)
        return token

    def fill(self, response, token):
        response.auth_token = token.auth_token
        response.renew_flag = token.renew_flag
        return response
