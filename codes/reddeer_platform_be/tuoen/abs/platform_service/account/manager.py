# coding=UTF-8

'''
Created on 2016年7月22日

@author: Administrator
'''

import datetime
import hashlib

from django.db.models import Q

from model.store.model_account import PlatformAccount, AgentAccount
from model.store.model_company import Company
from tuoen.abs.platform_service.company.manager import CompanyServer
from tuoen.abs.common_service.account import AccountServerBase
from tuoen.sys.core.exception.business_error import BusinessError
from tuoen.sys.utils.common.split_page import Splitor


class PlatformAccountServer(AccountServerBase):
    AccountModel = PlatformAccount

    @classmethod
    def generate_agent_main_account(cls, **account_create_info):
        return AgentAccount.create(**account_create_info)

    @classmethod
    def search(cls, current_page, **query_info):
        keywords = None
        if 'keywords' in query_info:
            keywords = query_info.pop('keywords')
        account_qs = AgentAccount.search(is_main=True).exclude(status=AgentAccount.Status.DELETE)
        if keywords:
            account_qs = account_qs.filter(
                Q(username__icontains=keywords) | Q(company__name__icontains=keywords))
        account_qs = account_qs.order_by('-create_time')
        return Splitor(current_page, account_qs, size=50)

    @classmethod
    def status_reverse(cls, agent_account):
        if agent_account.status:
            AgentAccount.search(company=agent_account.company).update(status=AgentAccount.Status.DISABLE)
        else:
            agent_account.update(status=AgentAccount.Status.ENABLE)

    @classmethod
    def delete(cls, account_id):
        agent_account = AgentAccount.search(id=account_id).\
            exclude(status=AgentAccount.Status.DELETE).first()
        if not agent_account:
            raise BusinessError('账号不存在')
        if agent_account.status:
            raise BusinessError('账号不是停用状态， 不能删除')
        AgentAccount.search(company=agent_account.company).update(status=AgentAccount.Status.DELETE)

        agent_account.company.update(status=Company.ComStatus.DELETE)

    @classmethod
    def reset_agent_password(cls, account_id):
        account = AgentAccount.search(id=account_id).\
            exclude(status=AgentAccount.Status.DELETE).first()
        if not account.is_main:
            raise BusinessError('重置的账号存在异常')
        default_password = hashlib.md5("abc123456".encode('utf8')).hexdigest()
        account.update(password=default_password)

    @classmethod
    def edit_agent_main_account(cls, account_id, edit_info):
        account = AgentAccount.search(id=account_id).\
            exclude(status=AgentAccount.Status.DELETE).first()
        company_info = {}
        if 'company_name' in edit_info:
            company_info['name'] = edit_info.pop('company_name')
        if 'company_phone' in edit_info:
            company_info['phone'] = edit_info.pop('company_phone')
        if 'company_address' in edit_info:
            company_info['address'] = edit_info.pop('company_address')
        company = Company.search(**company_info).first()
        if not company:
            account.company.update(**company_info)
        account.update(**edit_info)

    @classmethod
    def login(cls, username, password):
        """管理员登录"""
        b_account = PlatformAccount.search(username=username, password=password).first()
        a_account = AgentAccount.search(username=username, password=password).first()
        if not b_account and a_account:
            raise BusinessError("此处为管理员登录页， 普通用户账号请至普通登录页！")
        if not b_account:
            raise BusinessError("账号或密码错误")
        if b_account.status != PlatformAccount.Status.ENABLE:
            raise BusinessError("该账号已失效")

        b_account.update(last_login_time=datetime.datetime.now(), status=1)
        return b_account
