from datetime import datetime, timezone
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import AccessToken

from product.utils.response import response
from product.serializers.auth import UserSerializer
import jwt
from product.models import User
from rest_framework import status
from product.utils.status import unauthenticated


def validator(request):
    auth = request.headers.get('Authorization')
    res = response(request, data=unauthenticated,
                   status=status.HTTP_401_UNAUTHORIZED,
                   message="error")
    if not auth or not auth.startswith('Bearer'):
        raise AuthenticationFailed(detail=res)
    try:
        print(auth)
        token = auth.split(' ')[1]
        payload = jwt.decode(token, 'supersecretkey', algorithms=['HS256'])
    except jwt.InvalidTokenError:
        raise AuthenticationFailed(detail=res)

    user = User.objects.filter(id=payload['user_id']).first()
    serializer = UserSerializer(user)
    return serializer.data