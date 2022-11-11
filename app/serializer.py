from rest_framework import serializers
from app.models import Product, Cart, Order
from user.models import CustomUser


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id']


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'price']


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ['id', 'user', 'products']

    def to_representation(self, instance):
        self.fields['user'] = UserSerializer(read_only=True)
        self.fields['products'] = ProductSerializer(many=True, read_only=True)
        return super(CartSerializer, self).to_representation(instance)


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'user', 'cart']

    def to_representation(self, instance):
        self.fields['user'] = UserSerializer(read_only=True)
        self.fields['cart'] = CartSerializer(read_only=True)
        return super(OrderSerializer, self).to_representation(instance)
