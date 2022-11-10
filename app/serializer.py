from rest_framework import serializers
from app.models import Product, Cart, Order
from user.models import CustomUser


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id')


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'name', 'price')


class CartSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=True)
    products = ProductSerializer(many=True)

    class Meta:
        model = Cart
        fields = ('id', 'user', 'products')


class OrderSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=True)
    cart = CartSerializer(many=True)

    class Meta:
        model = Order
        fields = ('id', 'user', 'cart')
