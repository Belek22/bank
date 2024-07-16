from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework import status, generics, permissions
from .serializers import LoginSerializer, ReadUserSerializer, CreateUserSerializer, UpdateUserSerializer
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny, IsAuthenticated
from account.models import User
from rest_framework.views import APIView
from django.contrib.auth.hashers import check_password


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


class RedactorProfileApiView(RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = CreateUserSerializer
    lookup_field = 'pk'

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        password = request.data.get('password')
        if(password):
            if check_password(password, user.password):
                new_password = request.data.get('password1')
                user.set_password(new_password)
                user.save()
            else:
                return Response({'error': 'Пароль неверный'}, status=status.HTTP_400_BAD_REQUEST)
        token, created = Token.objects.get_or_create(user=user)
        user_serializer = UpdateUserSerializer(user, context={'request': request})
        return Response({
            **user_serializer.data,
            'token': token.key
        })
