import base64
import hmac
import time

import redis
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.pagination import CursorPagination
from rest_framework.response import Response
from rest_framework.serializers import ModelSerializer
from rest_framework.versioning import URLPathVersioning
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

# Create your views here.
from restful.models import Plugins
from restful.models import User
from restful.utils.redispool import pool


# from rest_framework import serializers


class MyPluginsPagination(CursorPagination):
    page_size = 5
    max_page_size = 10
    ordering = 'id'


class MyPluginsSerializer(ModelSerializer):
    class Meta:
        model = Plugins
        fields = ['id', 'name', 'type', 'size', 'brief']


class PluginsViewSet(ModelViewSet):
    # authentication_classes = [MyPluginsAuthentication]
    versioning_class = URLPathVersioning
    queryset = Plugins.objects.all()
    serializer_class = MyPluginsSerializer
    pagination_class = MyPluginsPagination

    # def list(self, request, *args, **kwargs):
    #     print('----------->', request)
    #     from rest_framework.response import Response
    #     for item in dir(request):
    #         try:
    #             print('==========>', getattr(request, item))
    #         except Exception as _:
    #             continue
    #     return Response('fuck you')


class MyUserSerializer(ModelSerializer):
    def validate_username(self, value):
        print('value==============>', value)
        return True

    class Meta:
        model = User
        fields = ['username']


class MyUserAuthentication(BaseAuthentication):
    def authenticate(self, request):
        user = request.query_params.get('user', None)
        print('in authentication current user is', user)
        if request.method == 'GET':
            token = request.query_params.get('token', None)
            # if certify_token(user, token):
            #     return
            try:
                r = redis.Redis(connection_pool=pool)
            except Exception as _:
                r = {}
            if r.get(user):
                return
            else:
                raise AuthenticationFailed('token is not right or expired')
        password = request.query_params.get('password', None)
        if user:
            user_obj = User.objects.filter(username=user, password=password)
            if user_obj:
                return user, user_obj
        raise AuthenticationFailed('user is not exist!')


def generate_token(key, expire=60):
    """

    :param key:
    :param expire:
    :return:
    """
    ex_time = str(time.time() + expire)
    ex_time_bytes = ex_time.encode('utf-8')
    sha1_hex_str = hmac.new(key.encode('utf-8'), ex_time_bytes, 'sha1').hexdigest()
    token = ex_time + ':' + sha1_hex_str
    b64_token = base64.urlsafe_b64encode(token.encode('utf-8'))
    return b64_token.decode('utf-8')


def certify_token(key, token):
    """

    :param key:
    :param token:
    :return:
    """
    if not token:
        return False
    token_str = base64.urlsafe_b64decode(token).decode('utf-8')
    ex_time, sha1_str = token_str.split(':')
    if ex_time < str(time.time()):
        return False
    ce_token = hmac.new(key.encode('utf-8'), ex_time.encode('utf-8'), 'sha1').hexdigest()
    if ce_token == sha1_str:
        return True
    return False


from rest_framework.parsers import JSONParser, FormParser
from rest_framework.throttling import SimpleRateThrottle


class MyUserThrottle(SimpleRateThrottle):
    scope = 'fuck'
    THROTTLE_RATES = {'fuck': '3/m'}

    def get_cache_key(self, request, view):
        print('current user is', request.user, view)
        return request.user


from rest_framework.permissions import BasePermission


class MyUserPermission(BasePermission):
    def has_permission(self, request, view):
        print('in permission current user is', request.user)
        return True
        # if request.method == 'POST' and request.user == 'dante':
        #     return True
        # return False


class UserView(APIView):
    versioning_class = URLPathVersioning
    # authentication_classes = [MyUserAuthentication]
    throttle_classes = [MyUserThrottle]
    # permission_classes = [MyUserPermission]

    # parser_classes = [JSONParser, FormParser]

    def get(self, request, *args, **kwargs):
        print('in get method current user is ', request.user)
        user_qs = User.objects.all()
        ret = MyUserSerializer(instance=user_qs, many=True)
        return Response(ret.data)

    def post(self, request, *args, **kwargs):
        print('in post method current user is', request.user, request.version)
        print('version', request.versioning_scheme.reverse('fuck_user', request=request))
        token = generate_token(request.user)
        r = redis.Redis(connection_pool=pool)
        r.set(request.user, token, ex=60)
        return Response(token)


from django.http.response import HttpResponse
from restful.forms import FileUpload

# def file_upload(request, *args, **kwargs):
#     if request.method == 'POST':
#         form = FileUpload(request.POST, request.FILES)
#         if form.is_valid():
#             handle_uploaded_file(request.FILES['file'])
#             return HttpResponse('success!!!')
#     else:
#         form = FileUpload()
#     return HttpResponse('failed!!!')
#
#
# def handle_uploaded_file(f):
#     with open(r'E:\temp\fuck.jpg', 'wb+') as destination:
#         for chunk in f.chunks():
#             destination.write(chunk)

from django.views.generic import FormView


class FileUpload(FormView):
    form_class = FileUpload
    template_name = 'upload.html'
    success_url = 'user'

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        files = request.FILES.getlist('file')
        print(len(files), form.fields, form.files)
        if form.is_valid():
            c = 0
            for f in files:
                with open(r'E:\temp\fuck_%d.jpg' % c, 'wb+') as d:
                    for chunk in f.chunks():
                        d.write(chunk)
                c += 1
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
