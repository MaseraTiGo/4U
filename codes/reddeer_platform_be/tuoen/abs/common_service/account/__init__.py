# -*- coding: UTF-8 -*-    
# Author: Dongjd
# FileName: __init__.py
# DateTime: 2020/12/17 18:30
# Project: awesome_dong
# Do Not Touch Me!

import datetime
import hashlib

from tuoen.abs.agent_service.role.manager import AgentRoleServer
from tuoen.sys.core.exception.business_error import BusinessError
from tuoen.sys.utils.common.split_page import Splitor


class AccountServerBase(object):
    AccountModel = None

    @classmethod
    def get_account_by_id(cls, account_id):
        account = cls.AccountModel.search(id=account_id). \
            exclude(status=cls.AccountModel.Status.DELETE).first()
        if not account:
            raise BusinessError("此账号不存在")
        return account

    @classmethod
    def generate_sub_account(cls, **account_create_info):
        if len(account_create_info['username']) > 20:
            raise BusinessError('账号名字超长')
        if not AgentRoleServer.is_role_valid(account_create_info.get('role')):
            raise BusinessError('角色处于不可用状态!')
        account = cls.get_account_by_username(account_create_info['username'])
        if account and account.status != cls.AccountModel.Status.DELETE:
            raise BusinessError('子账号已存在')
        else:
            account = cls.AccountModel.create(**account_create_info)
        return account

    @classmethod
    def login(cls, username, password):
        """员工登录"""
        account = cls.get_account_by_username(username)
        if account is None:
            raise BusinessError("账号或密码错误")

        if password != account.password:
            raise BusinessError("账号或密码错误")

        if not account.status:
            raise BusinessError("该账号已失效")

        account.update(last_login_time=datetime.datetime.now(), status=1)
        '''
        if settings.PERMISSION_CHECK:
            # if the type of account does not belong to the agent, then it has no the attribute of 'company'
            company_id = account.company.id if hasattr(account, 'company') and account.company else ''

            keys = [cls.AccountModel.__name__.lower(), str(account.role.id)]
            if company_id:
                keys = [cls.AccountModel.__name__.lower(), str(company_id), str(account.role.id)]
            role_store_key = '_'.join(keys)
            RuleMiddleware.store_2_redis(role_store_key, json.dumps(account.role.rules))
        '''
        return account

    @classmethod
    def update_account(cls, account, **update_info):
        """修改账号信息"""
        if 'username' in update_info:
            account_o = cls.get_account_by_username(update_info['username'])
            if account_o and account_o.id != account.id:
                raise BusinessError('用户名重复')
        account.update(**update_info)

    @classmethod
    def get_account_by_username(cls, username):
        """根据用户名判断账号对象是否存在"""
        account = cls.AccountModel.search(username=username). \
            exclude(status=cls.AccountModel.Status.DELETE).first()
        # if account is not None:
        #     raise BusinessError("该账号已存在")
        return account

    @classmethod
    def modify_password(cls, account, password, new_password):
        """修改员工密码"""
        if password != account.password:
            raise BusinessError("原密码错误")
        account.update(password=new_password)
        return True

    @classmethod
    def search(cls, current_page, only_sub=False):
        """查询账号列表"""
        if only_sub:
            account_list = cls.AccountModel.objects.filter(is_main=False)
        else:
            account_list = cls.AccountModel.query()
        account_list = account_list.order_by('-create_time')
        return Splitor(current_page, account_list, size=20)

    @classmethod
    def get_accounts_by_role(cls, role):
        return role.role_agent_accounts.all()

    @classmethod
    def reset_password(cls, account_id):
        account = cls.get_account_by_id(account_id)
        default_password = hashlib.md5("abc123456".encode('utf8')).hexdigest()
        account.update(password=default_password)
