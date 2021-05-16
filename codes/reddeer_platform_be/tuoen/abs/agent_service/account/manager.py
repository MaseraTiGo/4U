# coding=UTF-8

'''
Created on 2016年7月22日

@author: Administrator
'''

from model.models import AgentAccount
from tuoen.abs.common_service.account import AccountServerBase
from tuoen.sys.utils.common.split_page import Splitor
from tuoen.sys.core.exception.business_error import BusinessError


class AgentAccountServer(AccountServerBase):
    AccountModel = AgentAccount

    @classmethod
    def status_reverse(cls, account_id):
        account = cls.get_account_by_id(account_id)
        origin_status = account.status
        if origin_status:
            account.update(status=AgentAccount.Status.DISABLE)
        else:
            account.update(status=AgentAccount.Status.ENABLE)
        return origin_status
        # if account.is_main:
        #     accounts = cls.AccountModel.search(username__contains=account.username)
        #     if not account.status:
        #         account.update(**{'status': 1})
        #     else:
        #         accounts.update(**{'status': 0})
        # else:
        #     if account.status:
        #         account.update(**{'status': 0})
        #     else:
        #         account.update(**{'status': 1})

    @classmethod
    def search_my_sub(cls, current_page, **query_info):
        query_info.update({'is_main': False})
        account_qs = AgentAccount.search(**query_info).exclude(status=AgentAccount.Status.DELETE).order_by(
            '-create_time')
        return Splitor(current_page, account_qs, size=20)

    @classmethod
    def delete(cls, account_id):
        account = cls.get_account_by_id(account_id)
        if not account:
            raise BusinessError('账户不存在')
        if account.status:
            raise BusinessError('账户不处于停用状态， 不能删除')
        else:
            account.update(status=cls.AccountModel.Status.DELETE)

    @classmethod
    def edit_account(cls, account, **edit_info):
        if account.is_main:
            account_edit_info = {}
            if 'name' in edit_info:
                name = edit_info.pop('name')
                account_edit_info.update({'name': name})
            account.update(**account_edit_info)
            account.company.update(**edit_info)
        else:
            account.update(**edit_info)
