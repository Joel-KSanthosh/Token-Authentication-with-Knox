from knox.views import LoginView as KnoxLoginView
from knox.auth import TokenAuthentication
# from rest_framework import serializers

from django.contrib.auth import login,authenticate

# rest_framework imports
from rest_framework import generics, authentication, permissions
from rest_framework.settings import api_settings

from rest_framework.authentication import SessionAuthentication

from .serializers import UserSerializer,AuthSerializer,AuthToken
# Create your views here.


class CreateUserView(generics.CreateAPIView):
    serializer_class = UserSerializer


    

class LoginView(KnoxLoginView):
    serializer_class = AuthSerializer
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = AuthToken(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request,user)
        return super(LoginView,self).post(request, format)
