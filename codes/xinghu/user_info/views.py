from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response

from user_info.authentication import UserAuthenticator
from user_info.serializers import UserSerializer
from user_info.data_processor import user_info_query_set


# Create your views here.

@method_decorator(csrf_exempt, 'post')
class LoginView(APIView):
    authentication_classes = [UserAuthenticator]

    def post(self, request, **kwargs):
        return Response(f"welcome {request.user}, wish you have a nice day.")


class UserViewSet(ModelViewSet):
    queryset = user_info_query_set()
    serializer_class = UserSerializer
