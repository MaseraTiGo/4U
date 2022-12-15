# -*- coding: utf-8 -*-
# @File    : views.py
# @Project : x_web
# @Time    : 2022/12/14 13:58
# once, I want 2 leave my name 2 the history
# sadly, I find that my hair gets pale
"""                     
                                      /             
 __.  , , , _  _   __ ______  _    __/  __ ____  _, 
(_/|_(_(_/_</_/_)_(_)/ / / <_</_  (_/_ (_)/ / <_(_)_
                                                 /| 
                                                |/  
"""
from django.http import HttpResponse
from django.shortcuts import render

from super_dong.frame.core.api_doc import ApiDocGenerator


def api_doc(request):
    data = ApiDocGenerator.the_doke()
    return render(request, 'api_doc.html', {"data": data})
