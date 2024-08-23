from rest_framework import serializers

from product.models import Wishlist


class WishListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wishlist
        fields = ['id', 'product_id', 'user_id', 'created_at']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['created_at'] = instance.created_at.strftime('%Y-%m-%d')
        return representation


class WishlistListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Wishlist
        exclude = ['state', 'updated_at']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['created_at'] = instance.created_at.strftime('%Y-%m-%d %H:%M')
        return representation


class WishListDeleteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Wishlist
        fields = '__all__'