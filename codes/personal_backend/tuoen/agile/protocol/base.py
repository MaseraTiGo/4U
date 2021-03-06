# coding=UTF-8

import time

from tuoen.sys.core.protocol.base import BaseProtocol
from tuoen.sys.core.protocol.parser import Parser, ParseField
from tuoen.sys.core.protocol.responser import Responser, ResponseField
from tuoen.sys.core.field.base import CharField, IntField
from tuoen.sys.utils.common.signature import generate_signature, unique_parms
from tuoen.sys.core.exception.pro_error import ProtocolCodes, pro_errors


def _generate_signature(pro_parms, sign_key = 'sign'):
    unique_string , length = unique_parms(pro_parms, sign_key)
    return generate_signature(unique_string, length)


class DjangoProtocol(BaseProtocol):

    parser = Parser()
    parser.flag = ParseField(CharField, desc = "服务器标示")
    parser.api = ParseField(CharField, desc = "api标示")
    parser.timestamp = ParseField(IntField, desc = "时间戳")
    parser.sign = ParseField(CharField, desc = "协议签名")

    responser = Responser()
    responser.status = ResponseField(CharField, desc = "服务器状态")
    responser.msg = ResponseField(CharField, is_success = False, desc = "服务器错误消息")
    responser.code = ResponseField(CharField, is_success = False, desc = "服务器错误代码")

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

    def _check_timeout(self, pro_parms, all_parms, limit_seconds = 60):
        print('check protocol timeout...')
        client_time, vlalid_time = int(pro_parms.timestamp) , int(time.time()) - limit_seconds

        if client_time < vlalid_time:
            raise pro_errors(ProtocolCodes.PROTOCOL_TIMEROUT)
        return True

    def _check_sign(self, pro_parms, all_parms):
        return True
        print('check protocol signature...')
        if pro_parms.sign != _generate_signature(all_parms):
            raise pro_errors(ProtocolCodes.PROTOCOL_DATA_EXCHANGE)
        return True

    def extract_parms(self, pro):
        all_parms = {key: value for key, value in pro.POST.items()}

        meta = pro.META
        ip = meta['HTTP_X_FORWARDED_FOR'] \
                if 'HTTP_X_FORWARDED_FOR' in meta\
                    else meta['REMOTE_ADDR']

        base_parms = {
            self._upload_files: pro._files,
            self._ip: ip,
            self._agent: meta.get('HTTP_USER_AGENT', "")
        }
        return base_parms, all_parms

    def get_service_flag(self, pro_parms):
        return pro_parms.flag

    def get_api_flag(self, pro_parms):
        return pro_parms.api

    def get_success_parms(self, result):
        return {'status': 'ok'}

    def get_fail_parms(self, e):
        return {'status': e.get_flag(), 'msg': e.get_msg(), 'code': e.get_code()}
