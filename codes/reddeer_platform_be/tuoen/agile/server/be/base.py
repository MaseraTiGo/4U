# coding=UTF-8

from tuoen.sys.core.service.base import BaseAPIService


class AdminService(BaseAPIService):

    @classmethod
    def get_name(self):
        return "后台管理服务"

    @classmethod
    def get_desc(self):
        return "针对注册登录用户提供管理服务"

    @classmethod
    def get_flag(cls):
        return "admin"


admin_service = AdminService()

from tuoen.agile.platform_apis.account import Login, GenerateAgentAccount, AgentAccountList, \
    StatusReverse, Delete, ResetAgentPwd, EditAgentAccount, ChangePassword

admin_service.add(Login, GenerateAgentAccount, AgentAccountList, StatusReverse, Delete, ResetAgentPwd, EditAgentAccount,
                  ChangePassword)

# from tuoen.agile.platform_apis.role import Create

# admin_service.add(Create)

# from tuoen.agile.platform_apis.company import Create
#
# admin_service.add(Create)
