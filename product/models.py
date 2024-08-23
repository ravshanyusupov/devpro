from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=255, unique=True, db_index=True)
    password = models.CharField(max_length=255)
    avatar = models.CharField(max_length=255)
    username = None

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []

    class Meta:
        db_table = 'auth_users'


class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    price = models.DecimalField(decimal_places=2, max_digits=9)
    stock = models.IntegerField(default=0)
    state = models.IntegerField(default=1)
    user_id = models.BigIntegerField(null=False, blank=False, db_index=True)

    def __str__(self):
        return str(self.name)

    class Meta:
        db_table = 'seller_product'


class Wishlist(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    state = models.IntegerField(default=1)
    user_id = models.BigIntegerField(null=False, blank=False, db_index=True)
    product_id = models.BigIntegerField(null=False, blank=False)

    def __str__(self):
        return str(f"{User.objects.filter(id=self.user_id)}ning wishlisti")

    class Meta:
        db_table = 'wishlist'


