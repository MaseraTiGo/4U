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
from BuyGoods.restful_framework_utils.authentication import UserAuthentication
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.contrib.auth.middleware import AuthenticationMiddleware


class UsersViewSet(ModelViewSet):
    queryset = Users.objects.all()
    serializer_class = UsersSerializer
    pagination_class = UserPagination

    # authentication_classes = [UserAuthentication]

    # def __init__(self, *args, **kwargs):
    #     import time
    #     time.sleep(3)
    #     super().__init__(*args, **kwargs)

    @method_decorator(cache_page(10))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        print('in create current user is ', request.user)
        print('I know it must be null===========>', request.data, 'args', *args, 'kwargs', **kwargs)
        return Response('this is a fucking test!')

    def retrieve(self, request, *args, **kwargs):
        print('in retrieve data is---------->', *args, **kwargs)
        return Response('fuck you!')

    def post(self, request, *args, **kwargs):
        print('in post data is---------->', *args, **kwargs)

    def fuck(self):
        return Response('just a fucking test')
