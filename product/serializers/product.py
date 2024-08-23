from rest_framework import serializers
from ..models import Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'created_at', 'price', 'stock', 'user_id']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['created_at'] = instance.created_at.strftime('%Y-%m-%d')
        return representation


class UserListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['created_at'] = instance.created_at.strftime('%Y-%m-%d %H:%M')
        return representation


class ProductDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'created_at', 'user_id']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['created_at'] = instance.created_at.strftime('%Y-%m-%d %H:%M')
        return representation


class ProductUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'created_at', 'updated_at', 'user_id']
        extra_kwargs = {
            "created_at": {'read_only': True},
            "user_id": {'read_only': True},
            "id": {'read_only': True},
        }

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['updated_at'] = instance.updated_at.strftime('%Y-%m-%d %H:%M')
        representation['created_at'] = instance.created_at.strftime('%Y-%m-%d %H:%M')
        return representation


class ProductDeleteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = '__all__'