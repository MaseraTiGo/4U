from django.urls import path, include
from rest_framework.routers import DefaultRouter
from restful.views import PluginsViewSet
from restful.views import UserView
router = DefaultRouter()
router.register(r'plugins', PluginsViewSet)

urlpatterns = [
    path('user', UserView.as_view(), name='fuck_user'),
    path('', include(router.urls)),
]
