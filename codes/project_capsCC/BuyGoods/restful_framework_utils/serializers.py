# -*- coding: utf-8 -*-
# file_name       : serializers.py
# file_func       :
# file_author     : 'Johnathan.Wick'
# file_create_date: 2019/9/27 15:33

from rest_framework.serializers import ModelSerializer
from BuyGoods.models_store.goods import Goods


class GoodsSerializer(ModelSerializer):
    class Meta:
        model = Goods
        fields = ['name', 'sales', 'price', 'score', 'keywords']
