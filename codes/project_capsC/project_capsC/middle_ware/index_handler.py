# -*- coding: utf-8 -*-
# file_func  :
# file_author: 'Johnathan.Wick'
# file_date  : '6/12/2019 4:41 PM'

from ..models import Beauty


def index_handler(qs_lens=18):
    qs = Beauty.search()
    return qs
