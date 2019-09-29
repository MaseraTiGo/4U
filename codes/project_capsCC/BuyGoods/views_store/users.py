# -*- coding: utf-8 -*-
# file_name       : users.py
# file_func       :
# file_author     : 'Johnathan.Wick'
# file_create_date: 2019/9/29 9:04


from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response

from BuyGoods.models_store.members import Users
from BuyGoods.restful_framework_utils.serializers import UsersSerializer
from BuyGoods.restful_framework_utils.pagination import UserPagination


class UsersViewSet(ModelViewSet):
    queryset = Users.objects.all()
    serializer_class = UsersSerializer
    pagination_class = UserPagination

    # def create(self, request, *args, **kwargs):
    #     print('in create current user is ', request.user)
    #     print('I know it must be null===========>', request.data)
    #     return Response('this is a fucking test!')
