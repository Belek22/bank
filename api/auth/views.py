from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.contrib.auth import authenticate
from rest_framework import status, generics
from .serializers import LoginSerializer, ReadUserSerializer, CreateUserSerializer
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from account.models import User


class RegisterAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = CreateUserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token, created = Token.objects.get_or_create(user=user)
        read_serializer = ReadUserSerializer(user, context={'request': request})
        data = {**read_serializer.data, 'token': token.key}
        headers = self.get_success_headers(serializer.data)
        return Response(data, status=status.HTTP_201_CREATED, headers=headers)


class LoginApiView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data['username']
        password = serializer.validated_data['password']
        user = authenticate(username=username, password=password)

        if user:
            token, created = Token.objects.get_or_create(user=user)  # (token, False)
            read_serializer = ReadUserSerializer(user, context={'request': request})
            data = {**read_serializer.data, 'token': token.key}
            return Response(data)

        return Response({'detail': 'Не существует пользователя или неверный пароль.'},
                        status=status.HTTP_401_UNAUTHORIZED)