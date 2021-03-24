# -*- coding: utf-8 -*-

# ===================================
# file_name     : data_processor.py
# python_version: python 3.7.4
# file_author   : Johnathan.Strong
# create_time   : 2020/9/6 9:36
# ide_name      : PyCharm
# project_name  : xinghu
# ===================================

from user_info.models import UserInfoModel


def verify_current_account(user, password):
    user = UserInfoModel.objects.get(username=user)
    if user:
        return user.check_pasword(password)
    return False


def user_info_query_set():
    return UserInfoModel.objects.all()
