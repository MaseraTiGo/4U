# coding=UTF-8

from tuoen.abs.middleware.rule import rule_register, config_rules
from tuoen.sys.core.service.base import BaseAPIService


class UserService(BaseAPIService):

    @classmethod
    def get_name(cls):
        return "用户服务"

    @classmethod
    def get_desc(cls):
        return "针对注册登录用户提供服务"

    @classmethod
    def get_flag(cls):
        return "user"


user_service = UserService()
from tuoen.agile.agent_apis.file import Upload

user_service.add(Upload)

from tuoen.agile.agent_apis.config import Search, Update

user_service.add(Search, Update)
rule_register.register_api(config_rules.DEFAULT_CONFIG_QUERY, Search)
rule_register.register_api(config_rules.DEFAULT_CONFIG_EDIT, Update)

from tuoen.agile.agent_apis.account import Login, GenerateSubAccount, ChangePassword, SubAccountList, StatusReverse, \
    UpdateAccount, ResetPwd, Delete, EditAccount, AutoLogin, Get

user_service.add(Login, GenerateSubAccount, ChangePassword, SubAccountList, UpdateAccount, StatusReverse, ResetPwd,
                 Delete, EditAccount, AutoLogin, Get)

from tuoen.agile.agent_apis.role import Search, Edit, StatusReverse, Delete, Create, List

user_service.add(Search, Edit, StatusReverse, Delete, Create, List)

from tuoen.agile.agent_apis.landingpage import List, Copy, Rename, StatusChange, Create, Get, Edit, Publish, ListAll, \
    Delete, PublicGet, RelativeForm, PreView

user_service.add(List, Copy, Rename, StatusChange, Create, Get, Edit, Publish, ListAll, Delete, PublicGet, RelativeForm,
                 PreView)

from tuoen.agile.agent_apis.collection import List, Export, CollectInfo, TemplateList

user_service.add(List, Export, CollectInfo, TemplateList)

from tuoen.agile.agent_apis.form import Create, Delete, List, Search, Copy, Rename, Get, MultiGet, Publish, PublicGet, \
    PublicMultiGet, RelativeLandingPage, Edit, Fuzzy

user_service.add(Create, Delete, List, Search, Copy, Rename, Get, MultiGet, Publish, PublicGet, PublicMultiGet,
                 RelativeLandingPage, Edit, Fuzzy)
