from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.generics import ListAPIView, DestroyAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from ..serializers.wishlist import WishListSerializer, WishlistListSerializer, WishListDeleteSerializer
from product.utils.response import response
from product.utils.validators.token_validator import validator
from ..models import Wishlist
from ..utils.status import wishlist_not_found, wishlist_deleted


class WishListView(APIView):
    def post(self, request):
        user = validator(request)
        data = request.data
        data['user_id'] = user['id']
        serializer = WishListSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        res = response(request, serializer.data, status=status.HTTP_200_OK, message="ok")
        return Response(res)


class WishList(ListAPIView):
    serializer_class = WishlistListSerializer

    def get_queryset(self):
        user = validator(self.request)
        queryset = Wishlist.objects.filter(user_id=user['id'], state=1)
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        res = response(self.request, data=serializer.data, status=status.HTTP_200_OK, message="ok")
        return Response(res)


class WishListDelete(DestroyAPIView):
    queryset = Wishlist.objects.all()
    serializer_class = WishListDeleteSerializer

    def get_object(self):
        user = validator(self.request)
        wishlist_id = self.request.data['id']
        res = response(self.request, data=wishlist_not_found, status=status.HTTP_404_NOT_FOUND, message="error")
        try:
            wishlist = Wishlist.objects.get(id=wishlist_id, user_id=user['id'], state=1)
        except Wishlist.DoesNotExist:
            raise NotFound(detail=res)
        return wishlist

    def delete(self, request, *args, **kwargs):
        wishlist = self.get_object()
        data = {'state': 0}
        serializer = self.get_serializer(wishlist, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
        wishlist_deleted['message'] = f"Successfully deleted id of {wishlist.id}"
        res = response(request, data=wishlist_deleted, status=status.HTTP_200_OK, message="ok")
        return Response(res)