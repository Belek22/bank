from account.models import User
from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from django.contrib.auth.password_validation import validate_password


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)


class ReadUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ('password', 'user_permissions', 'groups')


class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ('password', 'user_permissions', 'groups', 'is_staff', 'is_active', 'is_superuser')

    username = serializers.CharField()
    last_name = serializers.CharField()
    first_name = serializers.CharField()
    date_of_birth = serializers.DateField()
    role = serializers.ChoiceField(choices=User.ROLE)
    avatar = serializers.ImageField()
    phone = serializers.CharField()
    email = serializers.EmailField()
    password1 = serializers.CharField(write_only=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True)

    experience = serializers.IntegerField(required=False)
    position = serializers.CharField(required=False, max_length=100)

    def validate(self, data):
        if data['password1'] != data['password2']:
            raise serializers.ValidationError({'password2': ["Пароли не совпадают."]})

        if data['role'] == User.BANKER:
            if 'experience' not in data or data['experience'] is None:
                raise serializers.ValidationError(
                    {'experience': ["Поле 'Опыт работы (лет)' обязательно для роли 'банкир'."]})
            if 'position' not in data or data['position'] is None:
                raise serializers.ValidationError({'position': ["Поле 'Должность' обязательно для роли 'банкир'."]})

        return data

    def create(self, validated_data):
        password = validated_data.pop('password1')
        validated_data.pop('password2')
        validated_data['password'] = make_password(password)

        return super().create(validated_data)



class UpdateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'date_of_birth', 'role', 'avatar', 'phone', 'email',
                'experience', 'position']

    def validate(self, data):
        if data.get('role') == User.BANKER:
            if 'experience' not in data or data['experience'] is None:
                raise serializers.ValidationError(
                        {'experience': ["Поле 'Опыт работы (лет)' обязательно для роли 'банкир'."]})
            if 'position' not in data or data['position'] is None:
                raise serializers.ValidationError({'position': ["Поле 'Должность' обязательно для роли 'банкир'."]})

        return data
