from django.urls import path, include
from rest_framework.routers import DefaultRouter
from restful.views import PluginsViewSet
router = DefaultRouter()
router.register(r'', PluginsViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
