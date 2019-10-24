from django.urls import path, include
from rest_framework.routers import DefaultRouter
from restful.views import PluginsViewSet
from restful.views import UserView
from restful.views import FileUpload
router = DefaultRouter()
router.register(r'plugins', PluginsViewSet)
app_name = 'restful'

urlpatterns = [
    path('user', UserView.as_view(), name='fuck_user'),
    path('file', FileUpload.as_view(), name='fuck_file'),
    path('', include(router.urls)),
]
