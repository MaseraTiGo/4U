# coding=UTF-8

'''
Created on 2016年7月23日

@author: Administrator
'''

import json
import itertools

from django.http.response import HttpResponse
from django.shortcuts import render_to_response

from tuoen.api.core.api import APIRouterProtocol
from tuoen.api.core.api_helper import api_helper
from tuoen.utils.exception.api_error import SYS_ERROR_CODES, SERVER_ERROR_CODES
from tuoen.utils.common import signature
from tuoen.middleware.oss import oss_register

from api.user.api import *


def _get_api_parameters(request):
    return {key: value for key, value in request.POST.items()}


def router(request):
    parms = _get_api_parameters(request)
    protocol = APIRouterProtocol()
    result = protocol.router(parms)
    resp = HttpResponse(json.dumps(result))
    resp['Access-Control-Allow-Origin'] = '*'  # 处理跨域请求
    return resp


def api_doc(request):
    error_codes = itertools.chain(SYS_ERROR_CODES, SERVER_ERROR_CODES)
    common_field_mappings = APIRouterProtocol._require_fileds
    all_server = api_helper.get_all_server()
    api_signature_doc = signature.__doc__
    return render_to_response("api_index.html", {
                            'error_codes': error_codes,
                            'all_server': all_server,
                            'common_field_mappings': common_field_mappings,
                            'auth_token': APIRouterProtocol._auth_filed,
                            'api_signature_doc': api_signature_doc,
                        })
