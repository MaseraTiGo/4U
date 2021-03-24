# -*- coding: utf-8 -*-

# ===================================
# file_name     : serializers.py
# python_version: python 3.7.4
# file_author   : Johnathan.Strong
# create_time   : 2020/9/6 10:25
# ide_name      : PyCharm
# project_name  : xinghu
# ===================================

from rest_framework.serializers import ModelSerializer

from user_info.models import UserInfoModel


class UserSerializer(ModelSerializer):
    class Meta:
        model = UserInfoModel
        fields = ['username', 'password', 'nickname', 'rank']
