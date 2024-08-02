from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework import status, generics, permissions
from .serializers import LoginSerializer, UserProfileSerializer, CreateUserSerializer, UpdateUserSerializer
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.request import Request
from rest_framework.viewsets import ViewSet
from rest_framework import viewsets
from account.models import User
from api.permissions import IsAdminOrReadOnly
from ..paginations import StandartPageNumberPagination


class RegisterAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = CreateUserSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token, created = Token.objects.get_or_create(user=user)
        read_serializer = UserProfileSerializer(user, context={'request': request})
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
            token, created = Token.objects.get_or_create(user=user)
            read_serializer = UserProfileSerializer(user, context={'request': request})
            data = {**read_serializer.data, 'token': token.key}
            return Response(data)

        return Response({'detail': 'Не существует пользователя или неверный пароль.'},
                        status=status.HTTP_401_UNAUTHORIZED)


class RedactorProfileApiView(ViewSet):
    queryset = User.objects.all()
    serializer_class = UpdateUserSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = UserProfileSerializer(user, context={'request': request})
        return Response(serializer.data)

    def post(self, request):
        return self._update(request)

    def put(self, request):
        return self._update(request)

    def patch(self, request):
        return self._update(request, partial=True)

    def _update(self, request, partial=False):
        instance = request.user
        serializer = self.get_serializer(instance=instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        token, created = Token.objects.get_or_create(user=user)
        data = {**serializer.data, 'token': token.key}
        return Response(serializer.data)


class UserProfileViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user



class BankersViewSet(viewsets.ModelViewSet):
    queryset = User.objects.filter(role=User.BANKER)
    serializer_class = UserProfileSerializer
    permission_classes = [IsAdminOrReadOnly]
    pagination_class = StandartPageNumberPagination
