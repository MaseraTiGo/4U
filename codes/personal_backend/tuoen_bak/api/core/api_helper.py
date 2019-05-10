# coding=UTF-8

'''
Created on 2016-6-28

@author: YRK
'''

import re
import inspect

from tuoen.utils.common.single import Single

__all__ = ["api_helper", "register",'SERVER_API_NAME','PATIENT_API_NAME',\
           'DOCTOR_API_NAME']

class TokenHelper(object):

    def __init__(self, token):
        self.token = token

    @property
    def is_expire(self):
        return self.token.is_expire

    @property
    def is_unvalid(self):
        return self.token is None

    def get_auth_user(self):
        return self.token.user
    
class API(object):

    def __init__(self, api_func, **config):
        self.parse(api_func)
        self.api_func = api_func
        self.name = self._get_domain_apiname()
        self.doc = api_func.__doc__
        self.is_auth = config.get('is_auth', True)
        
    @property
    def desc(self):
        result = re.search(r"@desc\s*[:|：]\s*(?P<last>\w+)", self.doc)
        if result:
            return result.groups()[0]
        return ""
    
    def bind_server(self, server):
        self.server = server

    def parse(self, ori_func):
        checker = inspect.getargspec(ori_func)
        default_size = len(checker.defaults) if checker.defaults else 0
        self.api_parm_fileds = checker.args[:] # 改值不允许更改
        self.required_size = len(self.api_parm_fileds) - default_size # 改值不允许更改

    def get_token_helper(self, auth_token):
        return None
        return TokenHelper(TokenManager.get_token(auth_token))

    def _get_domain_apiname(self):
        models = self.api_func.__module__.split('.')
        mods = list(filter(lambda mod: 'api' not in mod , models))
        mods.append(self.api_func.__name__)
        return '.'.join(mods)

    def execute(self, *args, **kwargs):
        return self.api_func(*args, **kwargs)

class APIHelper(Single):

    def __init__(self):
        self._register = {}

    def register(self, server, api):
        # todo: 此处应该判断是否有重复 api 注册
        if server.name not in self._register:
            self._register[server.name] = server
        server.register(api)
        return server

    def multi_register(self, servers, api):
        for server in servers:
            self.register(server, api)
            
#             # server register
#             if issubclass(server, BaseServer):
#                 self.register(server.__name__, api)
#             else:
#                 raise Exception("{server} server is not existed.".format(server = server))
        return servers, api

    def get_server(self, server_str):
        return self._register.get(server_str, None)
    
    def get_all_server(self):
        return self._register.values()

api_helper = APIHelper()

def api_register(*servers, **conf):
    def _api_register(func):
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        api_helper.multi_register(servers, API(func, **conf))
        return wrapper
    return _api_register


