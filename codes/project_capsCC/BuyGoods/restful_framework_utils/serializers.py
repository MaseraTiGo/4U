# -*- coding: utf-8 -*-
# file_name       : serializers.py
# file_func       :
# file_author     : 'Johnathan.Wick'
# file_create_date: 2019/9/27 15:33

import re

from rest_framework.exceptions import ValidationError
from rest_framework.serializers import ModelSerializer

from django.contrib.auth.hashers import make_password, check_password

from BuyGoods.models_store.goods import Goods
from BuyGoods.models_store.members import Users


class UsersSerializer(ModelSerializer):
    class Meta:
        model = Users
        fields = ['username', 'password', 'gender', 'brief', 'user_type', 'address']

    def validate_username(self, value):
        pattern = re.compile("^[\\u4e00-\\u9fa5a-zA-Z][\\u4e00-\\u9fa5a-zA-Z]+$")

        if len(value) <= 64 and pattern.search(value):
            return value
        else:
            raise ValidationError('data exception, too long or invalid character include')

    def validate_password(self, value):
        if 8 <= len(value) <= 16 and value.isalnum():
            return make_password(value)
        else:
            raise ValidationError('password is not valid!')


class GoodsSerializer(ModelSerializer):
    class Meta:
        model = Goods
        fields = ['name', 'sales', 'price', 'score', 'keywords']
