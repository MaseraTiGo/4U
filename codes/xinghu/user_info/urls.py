# -*- coding: utf-8 -*-

# ===================================
# file_name     : urls.py
# python_version: python 3.7.4
# file_author   : Johnathan.Strong
# create_time   : 2020/9/5 12:49
# ide_name      : PyCharm
# project_name  : xinghu
# ===================================

from django.urls import path, include
from rest_framework import routers

from user_info.views import LoginView
from user_info.views import UserViewSet

app_name = 'user_info'

router = routers.SimpleRouter()
router.register('', UserViewSet)

urlpatterns = [
    path('', include((router.urls, app_name))),
    path('login/', LoginView.as_view(), name='login'),

]
