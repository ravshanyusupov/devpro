from django.urls import path
from .views.auth import *
from .views.product import *
from .views.wishlist import *
from rest_framework_simplejwt.views import TokenRefreshView


urlpatterns = [
    path('v1/register', Register.as_view(), name='register'),
    path('v1/login', Login.as_view()),
    path('v1/change/password', ChangePassword.as_view()),
    path('v1/token/refresh', TokenRefreshView.as_view(), name='token-refresh'),
    path('v1/me', UserInfo.as_view()),


    path('v1/user/product/create', ProductView.as_view(), name='product'),
    path('v1/user/products', ProductList.as_view(), name='user-products'),
    path('v1/user/product/<int:pk>', ProductDetail.as_view(), name='product-detail'),
    path('v1/user/product/update', ProductUpdate.as_view(), name='product-update'),
    path('v1/user/product/delete', ProductDelete.as_view(), name='product-delete'),


    path('v1/wishlist', WishListView.as_view(), name='wishlist'),
    path('v1/wishlist/all', WishList.as_view(), name='wishlist-all'),
    path('v1/wishlist/delete', WishListDelete.as_view(), name='wishlist-delete'),
]