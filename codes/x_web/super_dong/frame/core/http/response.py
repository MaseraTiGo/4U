# -*- coding: utf-8 -*-
# @File    : response
# @Project : djangoProject
# @Time    : 2022/10/11 16:10
"""                     
                                      /             
 __.  , , , _  _   __ ______  _    __/  __ ____  _, 
(_/|_(_(_/_</_/_)_(_)/ / / <_</_  (_/_ (_)/ / <_(_)_
                                                 /| 
                                                |/  
"""
import dataclasses
import json

from django.http import HttpResponse, FileResponse


def file_yield(file_path, chunk_size=512):
    with open(file_path, mode='rb') as f:
        while True:
            c = f.read(chunk_size)
            if c:
                yield c
            else:
                break


def add_ex_resp_headers(resp):
    resp['Content-Type'] = 'application/json'
    resp['Access-Control-Allow-Origin'] = '*'
    resp['Access-Control-Max-Age'] = 86400
    resp['Access-Control-Allow-Methods'] = '*'
    resp['Access-Control-Allow-Headers'] = '*'
    return resp


@dataclasses.dataclass
class SuperDongResponse(object):
    rsp_data: dict
    ctn_type: str

    def http_response(self):
        return add_ex_resp_headers(HttpResponse(json.dumps(self.rsp_data)))

    def streaming_http_response(self):
        ...

    def file_response(self):
        return FileResponse(
            open(self.rsp_data['data']['File']['file_path'], 'rb'),
            as_attachment=True,
            filename=self.rsp_data['data']['File']['file_name']
        )

    @property
    def data(self):
        if self.ctn_type == 'application/json':
            return self.http_response()
        elif self.ctn_type == 'application/octet-stream':
            return self.file_response()

        return 'fucking placeholder'
