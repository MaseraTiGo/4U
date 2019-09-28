# -*- coding: utf-8 -*-
# file_name       : urls.py
# file_func       :
# file_author     : 'Johnathan.Wick'
# file_create_date: 2019/9/27 15:25

from django.urls import path
from BuyGoods.views_store.goods import goods

urlpatterns = [
    path('goods/', goods, name='goods'),
]
