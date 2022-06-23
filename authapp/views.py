from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from .renderers import UserJSONRenderer
from rest_framework import status
from rest_framework.generics import GenericAPIView,RetrieveUpdateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import (RegistrationSerializer,LoginSerializer,FndUserSerializer)
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from rest_framework.authentication import (
    TokenAuthentication,
    get_authorization_header
)
from django.conf import settings
from .authentication_handlers import*
from .models import *

# Create views here.
class RegistrationAPIView(APIView):
    
    permission_classes = (AllowAny,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = RegistrationSerializer
    
    def post(self, request):
       
        data = request.data

        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user = FndUser.objects.get(email=data.get("email"))
        token = AuthTokenHandler.create_auth_token(user)
        data["token"] = token.key
      
        return Response( status=status.HTTP_201_CREATED)


#login a user
class LoginApiView(GenericAPIView):
    permission_classes =(AllowAny,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = LoginSerializer

    def post(self,request):
        user = request.data

        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


#get a user and update
class FndUserRetrieveupdateApiView(RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = FndUserSerializer

    #get current logged in user
    def retrieve(self, request, *args, **kwargs):
        serializer = self.serializer_class(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)
        
    #update users
    def update(self, request, *args, **kwargs):
        serializer_data = request.data
        serializer = self.serializer_class(request.user, data = serializer_data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)













