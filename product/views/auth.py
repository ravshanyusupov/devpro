from rest_framework import status
from rest_framework.request import Request
from rest_framework.views import APIView
from ..serializers.auth import UserSerializer, TokenSerializer, ChangePasswordSerializer
from rest_framework.response import Response
from ..models import User
from rest_framework.exceptions import ParseError
from ..utils.response import response
from ..utils.status import user_not_found, invalid_request_body, old_password_incorrect, new_password_too_simple, \
    password_successfully_updated
from product.utils.validators.token_validator import validator
from rest_framework_simplejwt.tokens import RefreshToken
from ..utils.validators.password_validator import validate_password


class Register(APIView):

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        error = response(request, data=invalid_request_body,
                         status=status.HTTP_400_BAD_REQUEST,
                         message="error")
        if not serializer.is_valid():
            raise ParseError(detail=error)
        serializer.save()
        user = User.objects.filter(phone=serializer.data['phone']).first()
        token = RefreshToken.for_user(user)
        res = response(request, data={"refresh": str(token), "access": str(token.access_token), "type": "Bearer"}, status=status.HTTP_200_OK, message="ok")
        return Response(res)


class Login(APIView):
    serializer_class = TokenSerializer

    def post(self, request: Request, *args, **kwargs) -> Response:
        phone = request.data['phone']
        password = request.data['password']
        user = User.objects.filter(phone=phone).first()
        error = response(request, data=user_not_found,
                       status=status.HTTP_400_BAD_REQUEST,
                       message="error")
        if user is None:
            raise ParseError(detail=error)
        if not user.check_password(password):
            raise ParseError(detail=error)
        token = RefreshToken.for_user(user)
        res = response(request,
                       data={"refresh": str(token),
                             "access": str(token.access_token),
                             "type": "Bearer"},
                       status=status.HTTP_200_OK,
                       message="ok")
        return Response(res)


class ChangePassword(APIView):
    def put(self, request, *args, **kwargs):
        user = validator(request)
        old, new = request.data['old_password'], request.data['new_password']
        if not validate_password(new):
            error = response(request, data=new_password_too_simple, status=status.HTTP_400_BAD_REQUEST, message="error")
            raise ParseError(detail=error)
        if not request.user.check_password(old):
            error = response(request, data=old_password_incorrect, status=status.HTTP_400_BAD_REQUEST, message="error")
            raise ParseError(detail=error)
        serializer = ChangePasswordSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            request.user.set_password(serializer.validated_data['new_password'])
            request.user.save()
            res = response(request, data=password_successfully_updated, status=status.HTTP_200_OK, message="ok")
            return Response(res)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserInfo(APIView):
    def get(self, request):
        user = validator(request)
        res = response(request=request, data=user, status=status.HTTP_200_OK, message="ok")
        return Response(res)


