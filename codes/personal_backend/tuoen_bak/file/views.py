# coding=UTF-8

import json

from django.http.response import HttpResponse
from django.shortcuts import render_to_response
from .upload import UploadFileProtocol
# Create your views here.

def upload(request):
    result = UploadFileProtocol(request).excute()
    resp = HttpResponse(json.dumps(result))
    resp['Access-Control-Allow-Origin'] = '*'
    return resp
