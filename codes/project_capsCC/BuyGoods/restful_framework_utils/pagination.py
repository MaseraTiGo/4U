# -*- coding: utf-8 -*-
# file_name       : pagination.py
# file_func       :
# file_author     : 'Johnathan.Wick'
# file_create_date: 2019/9/29 9:23

from rest_framework.pagination import PageNumberPagination


class UserPagination(PageNumberPagination):
    page_size = 10
