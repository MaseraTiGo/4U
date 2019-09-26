from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
# Create your views here.
from restful.models import Plugins
from restful.models import User
from restful.models import Token
from rest_framework.serializers import ModelSerializer
from rest_framework.pagination import PageNumberPagination
from rest_framework.pagination import CursorPagination
from rest_framework.versioning import URLPathVersioning
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed

class MyPluginsAuthentication(BaseAuthentication):
    def authenticate(self, request):
        user = request.query_params.get('user', None)
        if user:
            user_obj = User.objects.filter(username=user)
            if user_obj:
                return (user, user_obj)
        raise AuthenticationFailed('user is not exist!')

class MyPluginsPagination(CursorPagination):
    page_size = 5
    max_page_size = 10
    ordering = 'id'

class MyPluginsSerializer(ModelSerializer):
    class Meta:
        model = Plugins
        fields = ['id', 'name', 'type', 'size', 'brief']

class PluginsViewSet(ModelViewSet):
    #authentication_classes = [MyPluginsAuthentication]
    versioning_class = URLPathVersioning
    queryset = Plugins.objects.all()
    serializer_class = MyPluginsSerializer
    pagination_class = MyPluginsPagination

    def list(self, request, *args, **kwargs):
        print('----------->', request)
        from rest_framework.response import Response
        for item in dir(request):
            try:
                print('==========>', getattr(request, item))
            except Exception as _:
                continue
        return Response('fuck you')
