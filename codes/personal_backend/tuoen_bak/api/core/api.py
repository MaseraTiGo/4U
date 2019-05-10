# coding=UTF-8

'''
Created on 2016-6-30

@author: YRK
'''

import time
import json

from tuoen.api.core.api_helper import api_helper
from tuoen.utils.exception.api_error import error_manager,APIBaseError
from tuoen.utils.exception.business_error import BusinessError

from tuoen.utils.potocol.custom_potocol import BaseCustomProtocol
from tuoen.utils.common.signature import generate_signature, unique_parms

from settings import DEBUG

APIException = error_manager.get_error

class APIRouterProtocol(BaseCustomProtocol):

    sign = None
    method = None
    timestamp = None

    _sign_key = "sign"
    _auth_filed = "auth_token"
    _inject_user_filed = "auth_user"

    _require_fileds = {
                        _sign_key:"算法暂未定，用于校验完整性",
                        "method":"指定的api调用名称，具体参详API文档",
                        "timestamp":"时间戳",
                   }

    def _generate_signature(self, parms):
        unique_string , length = unique_parms(parms, self._sign_key)
        return generate_signature(unique_string, length)

    def _verify_and_init_potocol(self, parms):
        if DEBUG:
            print('step 1 : check and init potocol')

        for field in self._require_fileds.keys():
            try:
                setattr(self, field, parms[field])
            except:
                raise APIException(10005)(field)
        return True

    def _verify_access_time(self, timestamp, limit_seconds = 60):
        if DEBUG:
            print('step 2 : verify_access_time')

        try:
            client_time , vlalid_time = int(timestamp) , int(time.time()) - limit_seconds
        except:
            raise APIException(20003)('timestamp')

        if client_time < vlalid_time:
            raise APIException(10004)()
        return True

    def _verify_data_integrality(self, parms):
        if DEBUG:
            print('step 3 : veriry_data_integrality')

        if parms[self._sign_key] != self._generate_signature(parms):
            raise APIException(10006)()
        return True

    def _verify_api_validity(self, api_func):
        if DEBUG:
            print('step 4 : verify api validity')

        print("【api name】 {}".format(api_func))
        try:
            server_str, api_func= api_func.split('.',1)
        except:
            raise APIException(10002)()

        server = api_helper.get_server(server_str)
        if server and api_func in server.apis:
            return server.apis[api_func]
        raise APIException(10002)()

    def _get_api_parameters(self, api, parms):
        if DEBUG:
            print('step 5 : verify api parameters')

        api_parms = {}

        api_parm_fileds, required_size = api.api_parm_fileds[:], api.required_size
        if api.is_auth:
            if self._auth_filed not in parms:
                raise APIException(10007)()

            auth_token = parms[self._auth_filed]
            token_helper = api.get_token_helper(auth_token)
            if token_helper.is_unvalid :
                raise APIException(10008)()

            if token_helper.is_expire:
                raise APIException(10009)()
            auth_user = token_helper.get_auth_user()
            api_parm_fileds.remove(self._inject_user_filed)
            api_parms.update({self._inject_user_filed:auth_user})
            required_size -= 1

            print("【auth user info】 id : {} , nick : {}".format(auth_user.id, auth_user.nick))

        # 必填字段
        for api_field in api_parm_fileds[:required_size]:
            try:
                api_parms[api_field] = parms[api_field]
            except:
                raise APIException(20002)(api_field)

        # 可选字段
        selectable_fields = {api_field : parms[api_field] for api_field in api_parm_fileds[required_size:] \
                             if api_field in parms}
        api_parms.update(selectable_fields)
        return api_parms

    def valid(self, parms):
        self._verify_and_init_potocol(parms)
        self._verify_access_time(self.timestamp)
        self._verify_data_integrality(parms)
        api = self._verify_api_validity(self.method)
        return api, self._get_api_parameters(api, parms)

    def _success(self, result):
        return {'status':1,'data':result}

    def _fail(self, result):
        response_result = {'status':0}
        response_result.update(result)
        return response_result

    def router(self, parms):
        try:
            api, api_parms = self.valid(parms)
            result = api.execute(**api_parms)
            result = self._success(result if result is not None else "")
            return result
        except (APIBaseError,BusinessError) as e:
            return self._fail(e())
        except Exception as e:
            return self._fail(APIException(10001)()())
