# -*- coding: utf-8 -*-
# @File    : __init__.py
# @Project : djangoProject
# @Time    : 2022/10/11 15:24
"""                     
                                      /             
 __.  , , , _  _   __ ______  _    __/  __ ____  _, 
(_/|_(_(_/_</_/_)_(_)/ / / <_</_  (_/_ (_)/ / <_(_)_
                                                 /| 
                                                |/  
"""
import json
from datetime import datetime

from django.conf import settings
from django.core.handlers.wsgi import WSGIRequest
from django.http.response import HttpResponse

from super_dong.frame.core.http.response import SuperDongResponse
from super_dong.frame.core.protocol import SuperDongProtocol
from super_dong.settings import PRINT_PREFIX


def debug_info(fn):
    def wrapper(*args, **kwargs):
        request = args[0]
        if settings.DEBUG:
            prefix = settings.PRINT_PREFIX if \
                hasattr(settings, 'PRINT_PREFIX') else PRINT_PREFIX

            print(
                f"\n{prefix}request From: "
                f"{request.META.get('REMOTE_ADDR', '-')} "
                f"At: {str(datetime.today()).split('.')[0]} To: {request.path_info} "
                f"Method: {request.method}"
            )
        ret = fn(*args, **kwargs)
        return ret

    return wrapper


@debug_info
def executor(request: WSGIRequest):
    try:
        ret_data, ctn_type = SuperDongProtocol.process_request(request)
        response_data = {
            'msg': None,
            'code': 0,
            'data': ret_data
        }
        return SuperDongResponse(response_data, ctn_type).data
    except IndexError as e:

        print(f"{PRINT_PREFIX} exception: {e}")
        response_data = {
            'msg': str(e),
            'code': -10000,
            'data': None
        }
    return HttpResponse(json.dumps(response_data))
