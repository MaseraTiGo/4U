# -*- coding: UTF-8 -*-    
# Author: Dongjd
# FileName: __init__.py
# DateTime: 2020/12/17 18:26
# Project: awesome_dong
# Do Not Touch Me!


from tuoen.sys.core.exception.business_error import BusinessError
from tuoen.sys.utils.common.split_page import Splitor
from tuoen.abs.middleware.role import role_middleware


class RoleServerBase(object):
    RoleModel = None
    AccountModel = None
    RelativesAccounts = None

    @classmethod
    def get_role_by_id(cls, role_id):
        role = cls.RoleModel.search(id=role_id).exclude(status=cls.RoleModel.Status.DELETE).first()
        if not role:
            raise BusinessError('该角色不存在！')
        return role

    @classmethod
    def get_role_by_name(cls, role_name):
        role = cls.RoleModel.search(name=role_name).first()
        if not role:
            raise BusinessError('该角色不存在！')
        return role

    @classmethod
    def search(cls, current_page, company):
        role_qs = cls.RoleModel.search(company=company).exclude(status=cls.RoleModel.Status.DELETE).order_by(
            '-create_time')
        return Splitor(current_page, role_qs, size=9999)

    @classmethod
    def delete_role_by_id(cls, role_id):
        role = cls.get_role_by_id(role_id)
        if not role.status:
            role_middleware.delete_redis(cls.RoleModel.__name__.lower(), role.id)
            role.update(status=cls.RoleModel.Status.DELETE)
        else:
            raise BusinessError("角色在使用中， 不能删除")

    @classmethod
    def create_role(cls, **create_info):
        role = cls.RoleModel.search(
            name=create_info.get('name'),
            company=create_info.get('company'),
        ).exclude(status=cls.RoleModel.Status.DELETE).first()
        if role:
            raise BusinessError('角色已存在')
        else:
            role = cls.RoleModel.create(**create_info)
            if not role:
                raise BusinessError('角色创建失败')
            else:
                role_middleware.set_redis(cls.RoleModel.__name__.lower(), role)
        return role

    @classmethod
    def create_admin_role_4_company(cls, company):
        return cls.RoleModel.create(name='admin', describe='this is an admin role', status=1, company=company)
