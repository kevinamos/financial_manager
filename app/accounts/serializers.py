import json
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from phonenumber_field import serializerfields
from django.contrib.auth import authenticate

from .models import User
from .token import get_jwt_token


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'username', 'id', 'first_name', 'last_name')


class RegistrationSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=False,
        validators=[UniqueValidator(
            queryset=User.objects.all(),
            message='Email already exists. '
                    'Please enter another email or sign in'
        )],
        error_messages={
            'invalid': 'Please enter a valid email address'
        }
    )
    phone_number = serializerfields.PhoneNumberField(
        required=False,
        validators=[UniqueValidator(
            queryset=User.objects.all(),
            message='PhoneNumber already exists. '
                    'Please enter another phonenumber or sign in'
        )],
    )
    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True,
        error_messages={
            'max_length': 'Password allows a maximum of 128 characters.',
            'min_length': 'Password allows a minimum of 8 characters.'
        })
    token = serializers.SerializerMethodField()

    def get_token(self, obj):
        if obj.phone_number:
            phone_obj = obj.phone_number
            code = '+' + str(phone_obj.country_code)
            number = str(phone_obj.national_number)
            phone_number = code + number

            class MyDict(dict):
                pass
            user = MyDict()
            user.username = phone_number
            user.phone_number = phone_number
            user.pk = str(obj.pk)
            token = get_jwt_token(user)
        else:
            token = get_jwt_token(obj)
        return token

    class Meta:
        model = User
        fields = ['email', 'phone_number', 'password', 'token']

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=False)
    phone_number = serializerfields.PhoneNumberField(required=False)
    password = serializers.CharField(max_length=128, write_only=True)
    token = serializers.CharField(read_only=True)

    def validate(self, data):
        email = data.get('email', None)
        phone_number = data.get('phone_number', None)
        password = data.get('password', None)

        if email is None and phone_number is None:
            raise serializers.ValidationError(
                'An email address or phone_number is required to log in.'
            )

        if password is None:
            raise serializers.ValidationError(
                'A password is required to log in.'
            )

        user = authenticate(username=phone_number or email, password=password)
        if user is None:
            raise serializers.ValidationError(
                'A user with this email/phone and password was not found.'
            )
        data['token'] = get_jwt_token(user)
        return data
