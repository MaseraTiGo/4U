# -*- coding: utf-8 -*-
# file_func  :
# file_author: 'Johnathan.Wick'
# file_date  : '6/12/2019 10:40 AM'

from django.shortcuts import render

from ..api.index import index as api_index


def index(request):
    index_data = api_index(request)
    content = {'img_s': index_data}
    return render(request, 'index.html', content)
