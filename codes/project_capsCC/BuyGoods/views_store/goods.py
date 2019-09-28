# -*- coding: utf-8 -*-
# file_name       : goods.py
# file_func       :
# file_author     : 'Johnathan.Wick'
# file_create_date: 2019/9/27 15:28
from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins
from rest_framework.response import Response


# class Goods(mixins.ListModelMixin, GenericViewSet):
#     pass
def goods(request):
    return Response('testing! forgive me')
