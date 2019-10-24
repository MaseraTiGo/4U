# -*- coding: utf-8 -*-
# file_name       : urls.py
# file_func       :
# file_author     : 'Johnathan.Wick'
# file_create_date: 2019/9/27 15:25

from django.urls import path, include
from BuyGoods.views_store.goods import goods
from rest_framework.routers import DefaultRouter
from BuyGoods.views_store.users import UsersViewSet

app_name = 'buy_goods'
router = DefaultRouter()
# router.register(r'goods/', goods, basename='buy_goods')
router.register('user', UsersViewSet, base_name='buy_user')

urlpatterns = [
    path('', include(router.urls)),
]
