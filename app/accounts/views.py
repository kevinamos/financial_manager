from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status
from rest_framework.renderers import JSONRenderer

from app.accounts.models import User
from app.accounts.serializers import (
    UserSerializer,
    RegistrationSerializer,
    LoginSerializer
)


class UserListView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class RegistrationView(generics.CreateAPIView):
    permission_classes = (AllowAny,)
    renderer_classes = (JSONRenderer,)
    serializer_class = RegistrationSerializer

    def post(self, request):
        payload = request.data
        if payload.get('email') is None and payload.get('phone_number') is None:
            msg = {
                'error': 'Please provide an email or phonenumber to register.'
            }
            return Response(msg, status=status.HTTP_400_BAD_REQUEST)
        serializer = self.serializer_class(data=payload)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class LoginView(generics.GenericAPIView):
    permission_classes = (AllowAny,)
    renderer_classes = (JSONRenderer,)
    serializer_class = LoginSerializer

    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
