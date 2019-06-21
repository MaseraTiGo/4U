# -*- coding: utf-8 -*-
# file_func  :
# file_author: 'Johnathan.Wick'
# file_date  : '6/18/2019 10:21 AM'


from ..middle_ware.index_handler import index_handler


def index(request):
    qs = index_handler()
    qs.order_by('-create_time')
    return qs
