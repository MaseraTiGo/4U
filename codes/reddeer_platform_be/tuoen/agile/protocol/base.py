# coding=UTF-8

import json

from tuoen.sys.core.field.base import CharField
from tuoen.sys.core.protocol.base import BaseProtocol
from tuoen.sys.core.protocol.parser import Parser, ParseField
from tuoen.sys.core.protocol.responser import Responser, ResponseField
from tuoen.sys.utils.common.signature import generate_signature, unique_parms


def _generate_signature(pro_parms, sign_key='sign'):
    unique_string, length = unique_parms(pro_parms, sign_key)
    return generate_signature(unique_string, length)


class DjangoProtocol(BaseProtocol):
    parser = Parser()
    parser.flag = ParseField(CharField, desc="服务标识")
    # parser.api = ParseField(CharField, desc="api标示")
    # parser.timestamp = ParseField(IntField, desc="时间戳")
    # parser.sign = ParseField(CharField, desc="协议签名")

    responser = Responser()
    responser.s = ResponseField(CharField, desc="状态码")
    responser.m = ResponseField(CharField, desc="错误消息")
    responser.d = ResponseField(CharField, desc="空字符")

    _sign_key = "sign"
    _upload_files = "_upload_files"
    _agent = "_agent"
    _ip = "_ip"

    @classmethod
    def get_name(cls):
        return "django-http"

    @classmethod
    def get_desc(cls):
        return "django框架接收http协议"

    def _check_timeout(self, pro_parms, all_parms, limit_seconds=60):
        # print('check protocol timeout...')
        # client_time, vlalid_time = int(pro_parms.timestamp), int(time.time()) - limit_seconds
        #
        # if client_time < vlalid_time:
        #     raise pro_errors(ProtocolCodes.PROTOCOL_TIMEROUT)
        return True

    def _check_sign(self, pro_parms, all_parms):
        return True
        # print('check protocol signature...')
        # if pro_parms.sign != _generate_signature(all_parms):
        #     raise pro_errors(ProtocolCodes.PROTOCOL_DATA_EXCHANGE)
        # return True

    @staticmethod
    def get_api_str(relative_path):
        return relative_path.replace('/interface/', '').rstrip('/')

    def extract_parms(self, pro):
        api_str = self.get_api_str(pro.META.get('PATH_INFO'))
        jwt_token = pro.META.get('HTTP_AUTHORIZATION')
        # all_parms = {key: value for key, value in pro.POST.items()}
        try:
            all_parms = {key: value for key, value in json.loads(pro.body.decode("utf-8")).items()}
        except:
            all_parms = {key: value for key, value in pro.POST.items()}
        all_parms.update({'api': api_str, 'jwt_token': jwt_token})
        meta = pro.META
        ip = meta['HTTP_X_FORWARDED_FOR'] \
            if 'HTTP_X_FORWARDED_FOR' in meta \
            else meta['REMOTE_ADDR']

        base_parms = {
            self._upload_files: pro.FILES if hasattr(pro, 'FILES') else '',
            self._ip: ip,
            self._agent: meta.get('HTTP_USER_AGENT', "")
        }
        print(f'dong ---------------->base params:\n {base_parms}')
        return base_parms, all_parms

    def get_service_flag(self, pro_parms):
        return pro_parms.flag

    def get_api_flag(self, pro_parms):
        return pro_parms.api

    def get_success_parms(self, result):
        return {'s': 0, 'm': '', 'd': result}

    def get_fail_parms(self, e):
        return {'s': -e.get_code(), 'm': e.get_msg(), 'd': ''}
