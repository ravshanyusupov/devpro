from rest_framework import serializers, status
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.exceptions import AuthenticationFailed, ParseError

from ..models import User
from ..utils.response import response
from ..utils.status import dont_match_both_password
from ..utils.validators.password_validator import validate_password
from ..utils.validators.phone_validator import validate_phone


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, min_length=8)
    phone = serializers.CharField(max_length=150, required=True, validators=[validate_phone,
                                                                                UniqueValidator(
                                                                                    queryset=User.objects.all(),
                                                                                    message=(
                                                                                        "username already exists"))])

    class Meta:
        model = User
        fields = ['id', 'name', 'phone', 'password', 'date_joined']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['date_joined'] = instance.date_joined.strftime('%Y-%m-%d')
        return representation

    def create(self, validate_data):
        password = validate_data.pop('password', None)
        instance = self.Meta.model(**validate_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    def validate(self, data):
        if data['old_password'] == data['new_password']:
            error = response(self.context['request'], data=dont_match_both_password, status=status.HTTP_400_BAD_REQUEST, message="error")
            raise ParseError(detail=error)
        return data


class TokenSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['user_id'] = user.id
        return token