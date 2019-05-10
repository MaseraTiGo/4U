# coding=UTF-8

'''
Created on 2016年7月23日

@author: FSY
'''

from tuoen.sys.core.field.base import CharField, DictField, IntField, ListField
from tuoen.sys.core.api.utils import with_metaclass
from tuoen.sys.core.api.request import RequestField, RequestFieldSet
from tuoen.sys.core.api.response import ResponseField, ResponseFieldSet
from tuoen.sys.core.exception.business_error import BusinessError

from tuoen.agile.apis.base import StaffAuthorizedApi
from tuoen.abs.service.account.manager import StaffAccountServer
from tuoen.abs.service.user.manager import StaffServer


class Password(StaffAuthorizedApi):
    """修改密码"""
    request = with_metaclass(RequestFieldSet)
    request.oldpassword = RequestField(CharField, desc = "当前未加密的登录密码")
    request.newpassword = RequestField(CharField, desc = "加密后的新登录密码")

    response = with_metaclass(ResponseFieldSet)

    @classmethod
    def get_desc(cls):
        return "员工修改密码接口"

    @classmethod
    def get_author(cls):
        return "fsy"

    def execute(self, request):
        staff = self.auth_user
        account = StaffAccountServer.get_account_bystaff(staff)
        StaffAccountServer.modify_password(account, request.oldpassword, request.newpassword)

    def fill(self, response):
        return response
