from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework.views import APIView
from ..serializers.product import ProductSerializer, UserListSerializer, ProductDetailSerializer, \
    ProductUpdateSerializer, ProductDeleteSerializer
from ..utils.response import response
from ..utils.status import product_not_found, deleted
from product.utils.validators.token_validator import validator
from rest_framework.generics import ListAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView
from ..models import Product


class ProductView(APIView):
    def post(self, request):
        user = validator(request)
        data = request.data
        data['user_id'] = user['id']
        serializer = ProductSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        res = response(request, serializer.data, status=status.HTTP_200_OK, message="ok")
        return Response(res)


class ProductList(ListAPIView):
    serializer_class = UserListSerializer

    def get_queryset(self):
        user = validator(self.request)
        queryset = Product.objects.filter(user_id=user['id'], state=1)
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        res = response(self.request, data=serializer.data, status=status.HTTP_200_OK, message="ok")
        return Response(res)


class ProductDetail(RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductDetailSerializer

    def get_object(self):
        product_id = self.kwargs.get('pk')
        user = validator(self.request)
        product = Product.objects.filter(id=product_id, user_id=user['id'], state=1).first()
        res = response(self.request, data=product_not_found, status=status.HTTP_404_NOT_FOUND, message="error")
        if not product:
            raise NotFound(detail=res)
        return product

    def retrieve(self, request, *args, **kwargs):
        product = self.get_object()
        serializer = self.get_serializer(product)
        res = response(self.request, data=serializer.data, status=status.HTTP_200_OK, message="ok")
        return Response(res)


class ProductUpdate(UpdateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductUpdateSerializer

    def get_object(self):
        product_id = self.request.data['id']
        user = validator(self.request)
        res = response(self.request, data=product_not_found, status=status.HTTP_404_NOT_FOUND, message="error")
        try:
            product = Product.objects.get(id=product_id, user_id=user['id'], state=1)
        except Product.DoesNotExist:
            raise NotFound(detail=res)
        return product

    def put(self, request, *args, **kwargs):
        product = self.get_object()
        serializer = self.get_serializer(product, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
        res = response(request, data=serializer.data, status=status.HTTP_200_OK, message="ok")
        return Response(res)


class ProductDelete(DestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductDeleteSerializer

    def get_object(self):
        user = validator(self.request)
        product_id = self.request.data['id']
        res = response(self.request, data=product_not_found, status=status.HTTP_404_NOT_FOUND, message="error")
        try:
            product = Product.objects.get(id=product_id, user_id=user['id'], state=1)
        except Product.DoesNotExist:
            raise NotFound(detail=res)
        return product

    def delete(self, request, *args, **kwargs):
        product = self.get_object()
        data = {'state': 0}
        serializer = self.get_serializer(product, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
        deleted['message'] = f"Successfully deleted id of {product.id}"
        res = response(request, data=deleted, status=status.HTTP_200_OK, message="ok")
        return Response(res)